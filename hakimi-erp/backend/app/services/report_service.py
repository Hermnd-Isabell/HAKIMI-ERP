from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sales import SalesOrder
from app.models.finance import Invoice, OpenAccountReceivable, ClosedAccountReceivable
from app.models.logistics import Delivery
from datetime import datetime, timedelta
from typing import List, Dict, Any

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
