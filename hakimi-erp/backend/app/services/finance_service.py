from sqlalchemy.orm import Session
from app.models.finance import Invoice, InvoiceItem, OpenAccountReceivable, ClosedAccountReceivable, Receipt
from app.models.logistics import Delivery, DeliveryItem
from app.schemas.finance import InvoiceCreate, ReceiptCreate
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal

class FinanceService:
    # --- Invoice ---
    @staticmethod
    def get_invoices(db: Session, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return db.query(Invoice).offset(skip).limit(limit).all()

    @staticmethod
    def get_invoice(db: Session, invoice_id: str) -> Optional[Invoice]:
        return db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()

    @staticmethod
    def create_invoice_from_delivery(db: Session, delivery_id: str) -> Invoice:
        # Fetch Delivery
        db_delivery = db.query(Delivery).filter(Delivery.delivery_id == delivery_id).first()
        if not db_delivery:
            raise Exception("Delivery not found")
        if db_delivery.delivery_status != "PGI_DONE":
            raise Exception("Invoice can only be created for deliveries with PGI_DONE status")
        
        # Check if invoice already exists for this delivery
        existing_invoice = db.query(Invoice).filter(Invoice.delivery_id == delivery_id).first()
        if existing_invoice:
            raise Exception(f"Invoice already exists for delivery {delivery_id}: {existing_invoice.invoice_id}")

        # Create Invoice Header
        invoice_id = f"INV{datetime.now().strftime('%y%m%d%H%M%S')}"
        db_invoice = Invoice(
            invoice_id=invoice_id,
            delivery_id=db_delivery.delivery_id,
            sales_order_id=db_delivery.sales_order_id,
            billing_type="F2",  # Standard Invoice
            invoice_date=date.today(),
            billing_date=date.today(),
            sold_to_party=db_delivery.ship_to_party, # Simplified
            payer=db_delivery.ship_to_party,        # Simplified
            currency="CNY",
            status="OPEN",
            total_amount=Decimal("0.00")
        )
        db.add(db_invoice)
        
        total_val = Decimal("0.00")
        # Create Invoice Items from Delivery Items
        for i, del_item in enumerate(db_delivery.items):
            # Try to get price from Sales Order Item if exists
            unit_price = Decimal("100.00") # Mock price if SO item not found
            if del_item.so_item_id:
                from app.models.sales import SalesOrderItem
                so_item = db.query(SalesOrderItem).filter(SalesOrderItem.so_item_id == del_item.so_item_id).first()
                if so_item:
                    unit_price = so_item.unit_price or unit_price
            
            net_val = unit_price * (del_item.delivery_quantity or 0)
            tax_val = net_val * Decimal("0.13")
            total_val += (net_val + tax_val)
            
            db_item = InvoiceItem(
                invoice_item_id=f"IVI{invoice_id[3:]}{i+1:02d}",
                invoice_id=invoice_id,
                item_no=(i + 1) * 10,
                material_id=del_item.material_id,
                quantity=del_item.delivery_quantity,
                unit_price=unit_price,
                tax_amount=tax_val,
                net_price=net_val
            )
            db.add(db_item)
            
        db_invoice.total_amount = total_val
        
        # Create Open AR
        db_ar = OpenAccountReceivable(
            open_ar_id=f"AR{invoice_id[3:]}",
            invoice_id=invoice_id,
            receivable_amount=total_val,
            received_amount=Decimal("0.00"),
            due_date=date.today(), # Simplified
            status="UNPAID"
        )
        db.add(db_ar)
        
        db.commit()
        db.refresh(db_invoice)
        return db_invoice

    # --- Account Receivables ---
    @staticmethod
    def get_open_ar(db: Session, skip: int = 0, limit: int = 100) -> List[OpenAccountReceivable]:
        return db.query(OpenAccountReceivable).offset(skip).limit(limit).all()

    @staticmethod
    def get_closed_ar(db: Session, skip: int = 0, limit: int = 100) -> List[ClosedAccountReceivable]:
        return db.query(ClosedAccountReceivable).offset(skip).limit(limit).all()

    # --- Receipt & Clearing ---
    @staticmethod
    def post_receipt(db: Session, receipt_in: ReceiptCreate) -> Receipt:
        # Create Receipt record
        data = receipt_in.model_dump()
        db_receipt = Receipt(**data)
        db.add(db_receipt)
        
        # Update AR
        db_ar = db.query(OpenAccountReceivable).filter(OpenAccountReceivable.invoice_id == receipt_in.invoice_id).first()
        if not db_ar:
            raise Exception("Open AR record not found for this invoice")
        
        db_ar.received_amount += receipt_in.receipt_amount
        
        # Check if fully cleared
        if db_ar.received_amount >= db_ar.receivable_amount:
            # Fully cleared: move to Closed AR
            db_closed = ClosedAccountReceivable(
                closed_ar_id=f"CAR{db_ar.open_ar_id[2:]}",
                invoice_id=db_ar.invoice_id,
                receivable_amount=db_ar.receivable_amount,
                received_amount=db_ar.received_amount,
                created_time=db_ar.created_time,
                closed_time=datetime.utcnow()
            )
            db.add(db_closed)
            
            # Update Invoice Status
            db_invoice = db_ar.invoice
            db_invoice.status = "CLEARED"
            
            # Remove from Open AR
            db.delete(db_ar)
        else:
            db_ar.status = "PARTIAL"
            db_ar.invoice.status = "PARTIAL"
            
        db.commit()
        db.refresh(db_receipt)
        return db_receipt

finance_service = FinanceService()
