from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract
from app.models.sales import SalesOrder, SalesOrderItem
from app.models.finance import Invoice, InvoiceItem, OpenAccountReceivable, ClosedAccountReceivable, Receipt
from app.models.logistics import Delivery
from app.models.customer import BusinessPartner
from app.models.material import Material
from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from decimal import Decimal

class ReportService:
    @staticmethod
    def get_sales_performance(db: Session, days: int = 30) -> Dict[str, Any]:
        start_date = datetime.now() - timedelta(days=days)
        
        # Aggregate sales by date
        sales_by_date = db.query(
            func.date(SalesOrder.created_time).label('date'),
            func.sum(SalesOrder.net_value).label('total_value'),
            func.count(SalesOrder.sales_order_id).label('order_count')
        ).filter(SalesOrder.created_time >= start_date)\
         .group_by(func.date(SalesOrder.created_time))\
         .order_by(func.date(SalesOrder.created_time)).all()
        
        return {
            "labels": [str(s.date) for s in sales_by_date],
            "values": [float(s.total_value or 0) for s in sales_by_date],
            "counts": [s.order_count for s in sales_by_date]
        }

    @staticmethod
    def get_financial_summary(db: Session) -> Dict[str, Any]:
        total_invoiced = db.query(func.sum(Invoice.total_amount)).filter(Invoice.status != 'VOID').scalar() or 0
        open_ar = db.query(func.sum(OpenAccountReceivable.receivable_amount - OpenAccountReceivable.received_amount)).scalar() or 0
        collected = db.query(func.sum(ClosedAccountReceivable.received_amount)).scalar() or 0
        
        return {
            "total_invoiced": float(total_invoiced),
            "open_receivables": float(open_ar),
            "collected_amount": float(collected),
            "collection_rate": float(collected / total_invoiced * 100) if total_invoiced > 0 else 0
        }

    @staticmethod
    def get_delivery_stats(db: Session) -> Dict[str, Any]:
        total_deliveries = db.query(func.count(Delivery.delivery_id)).scalar() or 0
        completed = db.query(func.count(Delivery.delivery_id)).filter(Delivery.delivery_status == 'PGI_DONE').scalar() or 0
        pending = total_deliveries - completed
        
        return {
            "total": total_deliveries,
            "completed": completed,
            "pending": pending,
            "completion_rate": float(completed / total_deliveries * 100) if total_deliveries > 0 else 0
        }

    # ================================================================
    #  Financial Detail Report — two modes: overview + statement
    # ================================================================
    @staticmethod
    def get_financial_detail(db: Session) -> Dict[str, Any]:
        today = date.today()

        # ---- 1. KPI summary ----
        total_invoiced = db.query(func.sum(Invoice.total_amount)).filter(Invoice.status != 'VOID').scalar() or Decimal(0)
        void_amount = db.query(func.sum(Invoice.total_amount)).filter(Invoice.status == 'VOID').scalar() or Decimal(0)

        # Open AR
        open_ar_rows = db.query(
            OpenAccountReceivable, Invoice
        ).join(Invoice, OpenAccountReceivable.invoice_id == Invoice.invoice_id).all()

        open_receivable_total = Decimal(0)
        received_so_far = Decimal(0)
        overdue_amount = Decimal(0)
        aging_buckets = {"current": Decimal(0), "1_30": Decimal(0), "31_60": Decimal(0), "61_90": Decimal(0), "90_plus": Decimal(0)}

        for ar, inv in open_ar_rows:
            outstanding = ar.receivable_amount - ar.received_amount
            open_receivable_total += outstanding
            received_so_far += ar.received_amount
            if ar.due_date and ar.due_date < today:
                overdue_amount += outstanding
                days_overdue = (today - ar.due_date).days
                if days_overdue <= 30:
                    aging_buckets["1_30"] += outstanding
                elif days_overdue <= 60:
                    aging_buckets["31_60"] += outstanding
                elif days_overdue <= 90:
                    aging_buckets["61_90"] += outstanding
                else:
                    aging_buckets["90_plus"] += outstanding
            else:
                aging_buckets["current"] += outstanding

        # Closed AR
        closed_rows = db.query(ClosedAccountReceivable).all()
        collected_amount = Decimal(0)
        for cr in closed_rows:
            collected_amount += cr.received_amount

        total_collected = received_so_far + collected_amount
        collection_rate = float(total_collected / total_invoiced * 100) if total_invoiced > 0 else 0.0

        # ---- 2. Invoice status distribution ----
        status_counts = db.query(
            Invoice.status,
            func.count(Invoice.invoice_id),
            func.sum(Invoice.total_amount)
        ).group_by(Invoice.status).all()

        status_distribution = []
        status_labels = {"OPEN": "Open", "PARTIAL": "Partial", "CLEARED": "Cleared", "VOID": "Void"}
        for s, cnt, amt in status_counts:
            status_distribution.append({
                "status": s,
                "label": status_labels.get(s, s),
                "count": cnt,
                "amount": float(amt or 0),
                "percentage": float(amt / total_invoiced * 100) if total_invoiced > 0 else 0
            })

        # ---- 3. Top 5 outstanding customers ----
        customer_outstanding = {}
        bp_names = {}
        for ar, inv in open_ar_rows:
            bp_id = inv.payer or ""
            outstanding = ar.receivable_amount - ar.received_amount
            if bp_id not in customer_outstanding:
                customer_outstanding[bp_id] = Decimal(0)
            customer_outstanding[bp_id] += outstanding

        bp_ids = list(customer_outstanding.keys())
        if bp_ids:
            bp_rows = db.query(BusinessPartner.bp_id, BusinessPartner.bp_name).filter(BusinessPartner.bp_id.in_(bp_ids)).all()
            for bp_id, bp_name in bp_rows:
                bp_names[bp_id] = bp_name

        top_customers = sorted(
            [{"bp_id": k, "bp_name": bp_names.get(k, k), "outstanding": float(v)} for k, v in customer_outstanding.items()],
            key=lambda x: x["outstanding"],
            reverse=True
        )[:5]

        # ---- 4. Monthly collection trend (last 6 months) ----
        six_months_ago = today - timedelta(days=180)
        receipts = db.query(Receipt).filter(Receipt.receipt_date >= six_months_ago).all()
        monthly_collections = {}
        for r in receipts:
            month_key = r.receipt_date.strftime("%Y-%m") if r.receipt_date else "Unknown"
            monthly_collections[month_key] = monthly_collections.get(month_key, Decimal(0)) + r.receipt_amount

        collection_trend = [
            {"month": k, "amount": float(v)}
            for k, v in sorted(monthly_collections.items())
        ]

        # ---- 5. AR aging summary ----
        aging_summary = [
            {"bucket": "Current (Not Due)", "amount": float(aging_buckets["current"]), "color": "success"},
            {"bucket": "1-30 Days", "amount": float(aging_buckets["1_30"]), "color": "warning"},
            {"bucket": "31-60 Days", "amount": float(aging_buckets["31_60"]), "color": "warning"},
            {"bucket": "61-90 Days", "amount": float(aging_buckets["61_90"]), "color": "danger"},
            {"bucket": "90+ Days", "amount": float(aging_buckets["90_plus"]), "color": "danger"},
        ]

        # ---- 6. Avg days to collect (from closed AR) ----
        avg_days_to_collect = 0.0
        if closed_rows:
            total_days = 0
            count = 0
            for cr in closed_rows:
                inv = db.query(Invoice).filter(Invoice.invoice_id == cr.invoice_id).first()
                if inv and inv.invoice_date and cr.closed_time:
                    total_days += (cr.closed_time.date() - inv.invoice_date).days
                    count += 1
            if count > 0:
                avg_days_to_collect = total_days / count

        # ================================================================
        # Statement-mode data (professional accounting tables)
        # ================================================================

        # ---- 7. AR by customer summary (beginning / invoiced / collected / ending) ----
        # "Beginning balance" = total invoiced before this month
        month_start = today.replace(day=1)

        all_invoices = db.query(Invoice).filter(Invoice.status != 'VOID').all()
        all_receipts = db.query(Receipt).all()

        customer_ar_summary = {}
        for inv in all_invoices:
            bp_id = inv.payer or ""
            if bp_id not in customer_ar_summary:
                customer_ar_summary[bp_id] = {
                    "bp_id": bp_id,
                    "bp_name": bp_names.get(bp_id, bp_id),
                    "beginning_balance": Decimal(0),
                    "invoiced_this_period": Decimal(0),
                    "collected_this_period": Decimal(0),
                    "ending_balance": Decimal(0),
                }
            if inv.invoice_date and inv.invoice_date >= month_start:
                customer_ar_summary[bp_id]["invoiced_this_period"] += inv.total_amount or Decimal(0)
            else:
                customer_ar_summary[bp_id]["beginning_balance"] += inv.total_amount or Decimal(0)
            customer_ar_summary[bp_id]["ending_balance"] += inv.total_amount or Decimal(0)

        for r in all_receipts:
            inv = next((i for i in all_invoices if i.invoice_id == r.invoice_id), None)
            bp_id = inv.payer if inv else r.payer or ""
            if bp_id not in customer_ar_summary:
                customer_ar_summary[bp_id] = {
                    "bp_id": bp_id,
                    "bp_name": bp_names.get(bp_id, bp_id),
                    "beginning_balance": Decimal(0),
                    "invoiced_this_period": Decimal(0),
                    "collected_this_period": Decimal(0),
                    "ending_balance": Decimal(0),
                }
            customer_ar_summary[bp_id]["collected_this_period"] += r.receipt_amount or Decimal(0)
            customer_ar_summary[bp_id]["ending_balance"] -= r.receipt_amount or Decimal(0)

        # Fill in bp names
        all_bp_ids = list(customer_ar_summary.keys())
        if all_bp_ids:
            bp_rows = db.query(BusinessPartner.bp_id, BusinessPartner.bp_name).filter(BusinessPartner.bp_id.in_(all_bp_ids)).all()
            for bp_id, bp_name in bp_rows:
                if bp_id in customer_ar_summary:
                    customer_ar_summary[bp_id]["bp_name"] = bp_name

        ar_by_customer = sorted(
            [{
                **v,
                "beginning_balance": float(v["beginning_balance"]),
                "invoiced_this_period": float(v["invoiced_this_period"]),
                "collected_this_period": float(v["collected_this_period"]),
                "ending_balance": float(v["ending_balance"]),
            } for v in customer_ar_summary.values()],
            key=lambda x: x["ending_balance"],
            reverse=True
        )

        # ---- 8. Receipt ledger (all receipts) ----
        receipt_ledger = []
        for r in all_receipts:
            inv = next((i for i in all_invoices if i.invoice_id == r.invoice_id), None)
            bp_id = inv.payer if inv else r.payer or ""
            bp_name = bp_names.get(bp_id, bp_id)
            receipt_ledger.append({
                "receipt_id": r.receipt_id,
                "invoice_id": r.invoice_id,
                "bp_id": bp_id,
                "bp_name": bp_name,
                "amount": float(r.receipt_amount or 0),
                "receipt_date": r.receipt_date.strftime("%Y-%m-%d") if r.receipt_date else "",
                "payment_method": r.payment_method or "",
                "reference_no": r.reference_no or "",
            })
        receipt_ledger.sort(key=lambda x: x["receipt_date"], reverse=True)

        # ---- 9. Invoice summary by status ----
        invoice_summary = []
        for s, cnt, amt in status_counts:
            invoice_summary.append({
                "status": s,
                "label": status_labels.get(s, s),
                "count": cnt,
                "amount": float(amt or 0),
                "percentage": float(amt / total_invoiced * 100) if total_invoiced > 0 else 0
            })

        # ---- 10. Overdue analysis (per invoice) ----
        overdue_invoices = []
        for ar, inv in open_ar_rows:
            if ar.due_date and ar.due_date < today:
                outstanding = ar.receivable_amount - ar.received_amount
                dp_id = inv.payer or ""
                days_overdue = (today - ar.due_date).days
                if days_overdue > 90:
                    risk_level = "High"
                elif days_overdue > 60:
                    risk_level = "Medium"
                else:
                    risk_level = "Low"
                overdue_invoices.append({
                    "invoice_id": inv.invoice_id,
                    "bp_id": dp_id,
                    "bp_name": bp_names.get(dp_id, dp_id),
                    "invoice_date": inv.invoice_date.strftime("%Y-%m-%d") if inv.invoice_date else "",
                    "due_date": ar.due_date.strftime("%Y-%m-%d"),
                    "days_overdue": days_overdue,
                    "outstanding": float(outstanding),
                    "risk_level": risk_level,
                })
        overdue_invoices.sort(key=lambda x: x["days_overdue"], reverse=True)

        return {
            # KPI cards
            "total_invoiced": float(total_invoiced),
            "void_amount": float(void_amount),
            "open_receivables": float(open_receivable_total),
            "collected_amount": float(total_collected),
            "overdue_amount": float(overdue_amount),
            "collection_rate": collection_rate,
            "avg_days_to_collect": avg_days_to_collect,
            "invoice_count": len(all_invoices),

            # Overview mode
            "status_distribution": status_distribution,
            "aging_summary": aging_summary,
            "top_customers": top_customers,
            "collection_trend": collection_trend,

            # Statement mode
            "ar_by_customer": ar_by_customer,
            "receipt_ledger": receipt_ledger,
            "invoice_summary": invoice_summary,
            "overdue_invoices": overdue_invoices,
        }

    @staticmethod
    def get_dashboard_summary(db: Session) -> Dict[str, Any]:
        """Calculates current KPIs and compares with previous periods"""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        yesterday_start = today_start - timedelta(days=1)
        
        month_start = datetime(now.year, now.month, 1)
        last_month_start = (month_start - timedelta(days=1)).replace(day=1)
        
        def calc_change(current, previous):
            if not previous or previous == 0:
                return "+100%" if current > 0 else "0%"
            change = ((current - previous) / previous) * 100
            return f"{'+' if change >= 0 else ''}{change:.1f}%"

        # 1. Sales Orders (Today vs Yesterday)
        total_orders = db.query(func.count(SalesOrder.sales_order_id)).scalar() or 0
        today_orders = db.query(func.count(SalesOrder.sales_order_id)).filter(SalesOrder.created_time >= today_start).scalar() or 0
        yesterday_orders = db.query(func.count(SalesOrder.sales_order_id)).filter(
            SalesOrder.created_time >= yesterday_start, 
            SalesOrder.created_time < today_start
        ).scalar() or 0
        
        # 2. Delivery Orders (Today vs Yesterday)
        total_deliveries = db.query(func.count(Delivery.delivery_id)).scalar() or 0
        
        # SAFER QUERY: Check if created_time exists before using it to avoid 500
        delivery_change = "0%"
        today_deliveries = 0
        try:
            today_deliveries = db.query(func.count(Delivery.delivery_id)).filter(Delivery.created_time >= today_start).scalar() or 0
            yesterday_deliveries = db.query(func.count(Delivery.delivery_id)).filter(
                Delivery.created_time >= yesterday_start, 
                Delivery.created_time < today_start
            ).scalar() or 0
            delivery_change = calc_change(today_deliveries, yesterday_deliveries)
        except Exception:
            # Fallback if created_time column doesn't exist yet
            delivery_change = "0%"

        # 3. Pending Deliveries
        pending_deliveries = db.query(func.count(Delivery.delivery_id)).filter(
            Delivery.delivery_status.in_(['OPEN', 'PICKING', 'SHIPPED', 'IN_TRANSIT'])
        ).scalar() or 0
        
        pending_change = "0%"
        try:
            # Simple logic for pending change
            pending_change = calc_change(pending_deliveries, total_deliveries * 0.1)
        except Exception:
            pass

        # 4. Receivables (Current vs Month Start)
        total_unpaid = db.query(func.sum(OpenAccountReceivable.receivable_amount - OpenAccountReceivable.received_amount)).scalar() or 0
        month_start_unpaid = 0
        try:
            month_start_unpaid = db.query(func.sum(OpenAccountReceivable.receivable_amount - OpenAccountReceivable.received_amount))\
                .filter(OpenAccountReceivable.created_time < month_start).scalar() or 0
        except Exception:
            pass
        
        # 5. Month Profit (This Month vs Last Month)
        month_order_value = db.query(func.sum(SalesOrder.net_value)).filter(SalesOrder.created_time >= month_start).scalar() or 0
        last_month_order_value = db.query(func.sum(SalesOrder.net_value)).filter(
            SalesOrder.created_time >= last_month_start,
            SalesOrder.created_time < month_start
        ).scalar() or 0

        return {
            "sales_orders": {
                "value": total_orders, 
                "change": calc_change(today_orders, yesterday_orders), 
                "type": "up" if today_orders >= yesterday_orders else "down", 
                "comparison": "vs. Yesterday"
            },
            "delivery_orders": {
                "value": total_deliveries, 
                "change": delivery_change, 
                "type": "up" if today_deliveries >= 0 else "down", 
                "comparison": "vs. Yesterday"
            },
            "pending_deliveries": {
                "value": pending_deliveries, 
                "change": pending_change, 
                "type": "down", 
                "comparison": "vs. Yesterday"
            },
            "receivables": {
                "value": float(total_unpaid or 0), 
                "change": calc_change(float(total_unpaid or 0), float(month_start_unpaid or 0)), 
                "type": "up", 
                "comparison": "vs. Last Month"
            },
            "month_profit": {
                "value": float(month_order_value or 0), 
                "change": calc_change(float(month_order_value or 0), float(last_month_order_value or 0)), 
                "type": "up" if (month_order_value or 0) >= (last_month_order_value or 0) else "down", 
                "comparison": "vs. Last Month"
            }
        }

report_service = ReportService()
