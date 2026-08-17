from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.finance import (
    Invoice, InvoiceItem, OpenAccountReceivable, ClosedAccountReceivable, Receipt
)
from app.models.logistics import Delivery
from app.models.sales import SalesOrder, SalesOrderItem, Quotation, Inquiry
from app.models.customer import BusinessPartner, CustomerFinanceData
from app.schemas.finance import InvoiceCreate, ReceiptCreate
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal
import re


class FinanceService:
    # -------------------------------------------------------------------- #
    #  Invoice
    # -------------------------------------------------------------------- #

    @staticmethod
    def get_invoices(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        customer: Optional[str] = None,
        invoice_no: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> Tuple[List[Invoice], int]:
        """C4+C5: 支持筛选 + 返回总条数"""
        query = db.query(Invoice)
        if customer:
            query = query.filter(
                or_(
                    Invoice.sold_to_party == customer,
                    Invoice.payer == customer,
                )
            )
        if invoice_no:
            query = query.filter(Invoice.invoice_id.ilike(f"%{invoice_no}%"))
        if status:
            query = query.filter(Invoice.status == status)
        if date_from:
            query = query.filter(Invoice.invoice_date >= date_from)
        if date_to:
            query = query.filter(Invoice.invoice_date <= date_to)

        total = query.count()
        items = (
            query.order_by(Invoice.invoice_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return items, total

    @staticmethod
    def get_invoice(db: Session, invoice_id: str) -> Optional[Invoice]:
        return db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()

    @staticmethod
    def _parse_payment_terms(payment_terms: Optional[str]) -> int:
        """C1: 解析付款条件字符串（如 'NET30'）返回天数"""
        if not payment_terms:
            return 30
        match = re.search(r"(\d+)", payment_terms)
        if match:
            return int(match.group(1))
        return 30

    @staticmethod
    def create_invoice_from_delivery(db: Session, delivery_id: str) -> Invoice:
        db_delivery = db.query(Delivery).filter(Delivery.delivery_id == delivery_id).first()
        if not db_delivery:
            raise Exception("Delivery not found")
        if db_delivery.delivery_status != "PGI_DONE":
            raise Exception("Invoice can only be created for deliveries with PGI_DONE status")

        existing = db.query(Invoice).filter(Invoice.delivery_id == delivery_id).first()
        if existing:
            raise Exception(f"Invoice already exists for delivery {delivery_id}: {existing.invoice_id}")

        # --- C1: 通过 SO 付款条件计算 due_date ---
        db_so = None
        if db_delivery.sales_order_id:
            db_so = db.query(SalesOrder).filter(
                SalesOrder.sales_order_id == db_delivery.sales_order_id
            ).first()

        payment_terms = db_so.payment_terms if db_so else None
        if not payment_terms and db_delivery.ship_to_party:
            fin = db.query(CustomerFinanceData).filter(
                CustomerFinanceData.bp_id == db_delivery.ship_to_party
            ).first()
            if fin:
                payment_terms = fin.payment_terms

        due_days = FinanceService._parse_payment_terms(payment_terms)
        invoice_date = date.today()
        due_date = invoice_date + timedelta(days=due_days)

        # --- 从 Inquiry 链路获取 sales_org / distribution_channel / division ---
        sales_org = distribution_channel = division = None
        if db_so and db_so.quotation_id:
            db_q = db.query(Quotation).filter(Quotation.quotation_id == db_so.quotation_id).first()
            if db_q and db_q.inquiry_id:
                db_inq = db.query(Inquiry).filter(Inquiry.inquiry_id == db_q.inquiry_id).first()
                if db_inq:
                    sales_org = db_inq.sales_org
                    distribution_channel = db_inq.distribution_channel
                    division = db_inq.division

        # --- destination_country 从 BP 获取 ---
        destination_country = None
        if db_delivery.ship_to_party:
            db_bp = db.query(BusinessPartner).filter(
                BusinessPartner.bp_id == db_delivery.ship_to_party
            ).first()
            if db_bp:
                destination_country = db_bp.country

        # --- 创建发票抬头 ---
        invoice_id = f"INV{datetime.now().strftime('%y%m%d%H%M%S')}"
        db_invoice = Invoice(
            invoice_id=invoice_id,
            delivery_id=db_delivery.delivery_id,
            sales_order_id=db_delivery.sales_order_id,
            billing_type="F2",
            invoice_date=invoice_date,
            billing_date=invoice_date,
            sales_org=sales_org,
            distribution_channel=distribution_channel,
            division=division,
            shipping_point=db_delivery.shipping_point,
            sold_to_party=db_delivery.ship_to_party,
            payer=db_delivery.ship_to_party,
            destination_country=destination_country,
            currency="CNY",
            status="OPEN",
            total_amount=Decimal("0.00"),
        )
        db.add(db_invoice)

        # --- 创建发票行项 ---
        total_val = Decimal("0.00")
        for i, del_item in enumerate(db_delivery.items):
            unit_price = Decimal("100.00")
            if del_item.so_item_id:
                so_item = db.query(SalesOrderItem).filter(
                    SalesOrderItem.so_item_id == del_item.so_item_id
                ).first()
                if so_item:
                    unit_price = so_item.unit_price or unit_price

            net_val = unit_price * (del_item.delivery_quantity or 0)
            tax_val = net_val * Decimal("0.13")
            total_val += net_val + tax_val

            db_item = InvoiceItem(
                invoice_item_id=f"IVI{invoice_id[3:]}{i + 1:02d}",
                invoice_id=invoice_id,
                item_no=(i + 1) * 10,
                material_id=del_item.material_id,
                quantity=del_item.delivery_quantity,
                sales_unit=del_item.sales_unit,
                unit_price=unit_price,
                tax_amount=tax_val,
                net_price=net_val,
                item_description=del_item.item_description,
            )
            db.add(db_item)

        db_invoice.total_amount = total_val

        # --- 创建 Open AR（due_date 由 C1 逻辑计算） ---
        db_ar = OpenAccountReceivable(
            open_ar_id=f"AR{invoice_id[3:]}",
            invoice_id=invoice_id,
            receivable_amount=total_val,
            received_amount=Decimal("0.00"),
            due_date=due_date,
            status="UNPAID",
        )
        db.add(db_ar)

        db.commit()
        db.refresh(db_invoice)
        return db_invoice

    @staticmethod
    def void_invoice(db: Session, invoice_id: str) -> Invoice:
        """D2: 发票冲销 — 仅 OPEN 状态可冲销"""
        db_invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
        if not db_invoice:
            raise Exception("Invoice not found")
        if db_invoice.status != "OPEN":
            raise Exception(f"Only OPEN invoices can be voided, current status: {db_invoice.status}")

        # 删除关联的 OpenAR（禁止物理删除业务单据 → 但 AR 是子记录，冲销时清理）
        if db_invoice.open_ar:
            db.delete(db_invoice.open_ar)

        db_invoice.status = "VOID"
        db.commit()
        db.refresh(db_invoice)
        return db_invoice

    @staticmethod
    def get_document_flow(db: Session, invoice_id: str) -> Dict[str, Any]:
        """D3: 单据流追溯 SO → Delivery → Invoice → Receipts → AR"""
        db_invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
        if not db_invoice:
            raise Exception("Invoice not found")

        flow: Dict[str, Any] = {"invoice": {"invoice_id": db_invoice.invoice_id, "status": db_invoice.status}}

        # Sales Order
        if db_invoice.sales_order_id:
            db_so = db.query(SalesOrder).filter(
                SalesOrder.sales_order_id == db_invoice.sales_order_id
            ).first()
            if db_so:
                flow["sales_order"] = {
                    "sales_order_id": db_so.sales_order_id,
                    "status": db_so.status,
                    "customer_id": db_so.customer_id,
                    "net_value": float(db_so.net_value) if db_so.net_value else None,
                }

        # Delivery
        if db_invoice.delivery_id:
            db_del = db.query(Delivery).filter(Delivery.delivery_id == db_invoice.delivery_id).first()
            if db_del:
                flow["delivery"] = {
                    "delivery_id": db_del.delivery_id,
                    "delivery_status": db_del.delivery_status,
                    "ship_to_party": db_del.ship_to_party,
                }

        # Receipts
        receipts = db.query(Receipt).filter(Receipt.invoice_id == invoice_id).all()
        if receipts:
            flow["receipts"] = [
                {
                    "receipt_id": r.receipt_id,
                    "receipt_amount": float(r.receipt_amount),
                    "receipt_date": r.receipt_date.isoformat() if r.receipt_date else None,
                    "payment_method": r.payment_method,
                }
                for r in receipts
            ]

        # AR 状态
        if db_invoice.open_ar:
            flow["account_receivable"] = {
                "type": "open",
                "open_ar_id": db_invoice.open_ar.open_ar_id,
                "receivable_amount": float(db_invoice.open_ar.receivable_amount),
                "received_amount": float(db_invoice.open_ar.received_amount),
                "due_date": db_invoice.open_ar.due_date.isoformat() if db_invoice.open_ar.due_date else None,
                "status": db_invoice.open_ar.status,
            }
        elif db_invoice.closed_ar:
            car = db_invoice.closed_ar[-1] if isinstance(db_invoice.closed_ar, list) else db_invoice.closed_ar
            flow["account_receivable"] = {
                "type": "closed",
                "closed_ar_id": car.closed_ar_id,
                "receivable_amount": float(car.receivable_amount),
                "received_amount": float(car.received_amount),
                "status": "CLEARED",
            }

        return flow

    # -------------------------------------------------------------------- #
    #  Account Receivables
    # -------------------------------------------------------------------- #

    @staticmethod
    def get_open_ar(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        customer: Optional[str] = None,
        invoice_no: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Tuple[List[OpenAccountReceivable], int]:
        """C4+C5: 分页 + 筛选"""
        query = db.query(OpenAccountReceivable)
        if customer:
            query = query.join(Invoice).filter(
                or_(Invoice.sold_to_party == customer, Invoice.payer == customer)
            )
        if invoice_no:
            query = query.filter(OpenAccountReceivable.invoice_id.ilike(f"%{invoice_no}%"))
        if status:
            query = query.filter(OpenAccountReceivable.status == status)

        total = query.count()
        items = query.order_by(OpenAccountReceivable.created_time.desc()).offset(skip).limit(limit).all()
        return items, total

    @staticmethod
    def get_closed_ar(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        customer: Optional[str] = None,
        invoice_no: Optional[str] = None,
    ) -> Tuple[List[ClosedAccountReceivable], int]:
        """C4+C5: 分页 + 筛选"""
        query = db.query(ClosedAccountReceivable)
        if customer:
            query = query.join(Invoice).filter(
                or_(Invoice.sold_to_party == customer, Invoice.payer == customer)
            )
        if invoice_no:
            query = query.filter(ClosedAccountReceivable.invoice_id.ilike(f"%{invoice_no}%"))

        total = query.count()
        items = query.order_by(ClosedAccountReceivable.closed_time.desc()).offset(skip).limit(limit).all()
        return items, total

    @staticmethod
    def get_open_ar_by_invoice(db: Session, invoice_id: str) -> Optional[OpenAccountReceivable]:
        """D4: 按发票精确查询未清 AR"""
        return db.query(OpenAccountReceivable).filter(
            OpenAccountReceivable.invoice_id == invoice_id
        ).first()

    @staticmethod
    def get_closed_ar_by_invoice(db: Session, invoice_id: str) -> List[ClosedAccountReceivable]:
        """D4: 按发票精确查询已清 AR"""
        return db.query(ClosedAccountReceivable).filter(
            ClosedAccountReceivable.invoice_id == invoice_id
        ).all()

    # -------------------------------------------------------------------- #
    #  Receipt & Clearing
    # -------------------------------------------------------------------- #

    @staticmethod
    def get_receipts(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        invoice_no: Optional[str] = None,
        payer: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> Tuple[List[Receipt], int]:
        """D1: 收款列表 — 分页 + 筛选"""
        query = db.query(Receipt)
        if invoice_no:
            query = query.filter(Receipt.invoice_id.ilike(f"%{invoice_no}%"))
        if payer:
            query = query.filter(Receipt.payer == payer)
        if date_from:
            query = query.filter(Receipt.receipt_date >= datetime.combine(date_from, datetime.min.time()))
        if date_to:
            query = query.filter(Receipt.receipt_date <= datetime.combine(date_to, datetime.max.time()))

        total = query.count()
        items = query.order_by(Receipt.receipt_date.desc()).offset(skip).limit(limit).all()
        return items, total

    @staticmethod
    def get_receipt(db: Session, receipt_id: str) -> Optional[Receipt]:
        """D1: 收款详情"""
        return db.query(Receipt).filter(Receipt.receipt_id == receipt_id).first()

    @staticmethod
    def post_receipt(db: Session, receipt_in: ReceiptCreate) -> Receipt:
        """C2+C3: receipt_id 后端生成 + 全额核销后关闭 SO"""
        # 查发票
        db_invoice = db.query(Invoice).filter(Invoice.invoice_id == receipt_in.invoice_id).first()
        if not db_invoice:
            raise Exception("Invoice not found")
        if db_invoice.status == "VOID":
            raise Exception("Cannot post receipt for a voided invoice")

        # 查 Open AR
        db_ar = db.query(OpenAccountReceivable).filter(
            OpenAccountReceivable.invoice_id == receipt_in.invoice_id
        ).first()
        if not db_ar:
            raise Exception("Open AR record not found for this invoice")

        # C3: 后端生成 receipt_id，从发票推导 payer
        receipt_id = f"RCP{datetime.now().strftime('%y%m%d%H%M%S')}"
        db_receipt = Receipt(
            receipt_id=receipt_id,
            invoice_id=receipt_in.invoice_id,
            payer=db_invoice.payer,
            receipt_amount=receipt_in.receipt_amount,
            payment_method=receipt_in.payment_method,
            currency=receipt_in.currency,
            reference_no=receipt_in.reference_no,
            remark=receipt_in.remark,
            search_term=receipt_in.search_term,
        )
        db.add(db_receipt)

        # 更新 AR 已收金额
        db_ar.received_amount += receipt_in.receipt_amount

        if db_ar.received_amount >= db_ar.receivable_amount:
            # --- 全额核销 ---
            db_closed = ClosedAccountReceivable(
                closed_ar_id=f"CAR{db_ar.open_ar_id[2:]}",
                invoice_id=db_ar.invoice_id,
                receivable_amount=db_ar.receivable_amount,
                received_amount=db_ar.received_amount,
                created_time=db_ar.created_time,
                closed_time=datetime.utcnow(),
                remark=db_ar.remark,
                search_term=db_ar.search_term,
            )
            db.add(db_closed)

            db_invoice.status = "CLEARED"
            db.delete(db_ar)

            # C2: 关闭关联销售订单
            if db_invoice.sales_order_id:
                db_so = db.query(SalesOrder).filter(
                    SalesOrder.sales_order_id == db_invoice.sales_order_id
                ).first()
                if db_so:
                    db_so.status = "CLOSED"
        else:
            db_ar.status = "PARTIAL"
            db_invoice.status = "PARTIAL"

        db.commit()
        db.refresh(db_receipt)
        return db_receipt


finance_service = FinanceService()
