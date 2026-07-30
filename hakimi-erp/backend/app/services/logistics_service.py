from sqlalchemy.orm import Session
from app.models.logistics import Delivery, DeliveryItem, GoodsIssue
from app.models.sales import SalesOrder, SalesOrderItem
from app.schemas.logistics import DeliveryCreate, GoodsIssueCreate
from typing import List, Optional
from datetime import datetime

class LogisticsService:
    # --- Delivery ---
    @staticmethod
    def get_deliveries(db: Session, skip: int = 0, limit: int = 100) -> List[Delivery]:
        return db.query(Delivery).offset(skip).limit(limit).all()

    @staticmethod
    def get_delivery(db: Session, delivery_id: str) -> Optional[Delivery]:
        return db.query(Delivery).filter(Delivery.delivery_id == delivery_id).first()

    @staticmethod
    def create_delivery(db: Session, delivery_in: DeliveryCreate) -> Delivery:
        data = delivery_in.model_dump()
        items_data = data.pop("items")
        db_delivery = Delivery(**data)
        db.add(db_delivery)
        
        for item in items_data:
            db_item = DeliveryItem(**item, delivery_id=db_delivery.delivery_id)
            db.add(db_item)
            
        db.commit()
        db.refresh(db_delivery)
        return db_delivery

    @staticmethod
    def create_from_sales_order(db: Session, sales_order_id: str) -> Delivery:
        # Fetch Sales Order
        db_so = db.query(SalesOrder).filter(SalesOrder.sales_order_id == sales_order_id).first()
        if not db_so:
            raise Exception("Sales Order not found")
        
        # Create Delivery Header
        delivery_id = f"DEL{datetime.now().strftime('%y%m%d%H%M%S')}"
        db_delivery = Delivery(
            delivery_id=delivery_id,
            sales_order_id=db_so.sales_order_id,
            delivery_type="LF",  # Standard Delivery
            delivery_status="OPEN",
            ship_to_party=db_so.ship_to_party or db_so.customer_id,
            planned_delivery_date=db_so.requested_delivery_date,
            shipping_point=db_so.delivering_plant
        )
        db.add(db_delivery)
        
        # Create Delivery Items from SO Items
        for i, so_item in enumerate(db_so.items):
            db_item = DeliveryItem(
                delivery_item_id=f"DI{delivery_id[3:]}{i+1:02d}",
                delivery_id=delivery_id,
                item_no=(i + 1) * 10,
                so_item_id=so_item.so_item_id,
                material_id=so_item.material_id,
                delivery_quantity=so_item.order_quantity,
                sales_unit=so_item.sales_unit,
                item_description=f"Delivery for SO {sales_order_id} Item {so_item.item_no}"
            )
            db.add(db_item)
            
        db.commit()
        db.refresh(db_delivery)
        return db_delivery

    # --- PGI (Post Goods Issue) ---
    @staticmethod
    def post_goods_issue(db: Session, delivery_id: str) -> Delivery:
        db_delivery = db.query(Delivery).filter(Delivery.delivery_id == delivery_id).first()
        if not db_delivery:
            raise Exception("Delivery not found")
        
        if db_delivery.delivery_status == "PGI_DONE":
            raise Exception("Goods Issue already posted for this delivery")
        
        # Create GoodsIssue record for each item
        for item in db_delivery.items:
            gi_id = f"PGI{datetime.now().strftime('%y%m%d%H%M%S')}{item.item_no}"
            db_gi = GoodsIssue(
                goods_issue_id=gi_id,
                delivery_item_id=item.delivery_item_id,
                actual_quantity=item.delivery_quantity,
                posting_date=datetime.now().date(),
                warehouse=item.delivery.shipping_point
            )
            db.add(db_gi)
            
        # Update Delivery Status
        db_delivery.delivery_status = "PGI_DONE"
        db_delivery.actual_gi_date = datetime.now()
        
        db.commit()
        db.refresh(db_delivery)
        return db_delivery

logistics_service = LogisticsService()
