from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Integer, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Delivery(Base):
    __tablename__ = "delivery"

    delivery_id = Column(String(20), primary_key=True)
    sales_order_id = Column(String(20), ForeignKey("sales_order.sales_order_id"))
    delivery_type = Column(String(20), nullable=False)
    delivery_status = Column(String(20), nullable=False, comment="OPEN/PGI_DONE/CANCELLED")
    ship_to_party = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    planned_delivery_date = Column(Date)
    planned_gi_date = Column(Date)
    actual_gi_date = Column(DateTime)
    picking_date = Column(Date)
    shipping_point = Column(String(20))

    items = relationship("DeliveryItem", back_populates="delivery", cascade="all, delete-orphan")

class DeliveryItem(Base):
    __tablename__ = "delivery_item"

    delivery_item_id = Column(String(20), primary_key=True)
    delivery_id = Column(String(20), ForeignKey("delivery.delivery_id"), nullable=False)
    item_no = Column(Integer, nullable=False)
    so_item_id = Column(String(20), ForeignKey("sales_order_item.so_item_id"))
    material_id = Column(String(20), ForeignKey("material.material_id"), nullable=False)
    delivery_quantity = Column(DECIMAL(15,3))
    sales_unit = Column(String(10))
    item_description = Column(String(255))

    __table_args__ = (UniqueConstraint('delivery_id', 'item_no', name='uk_delivery_item'),)

    delivery = relationship("Delivery", back_populates="items")
    goods_issues = relationship("GoodsIssue", back_populates="delivery_item")

class GoodsIssue(Base):
    __tablename__ = "goods_issue"

    goods_issue_id = Column(String(20), primary_key=True)
    delivery_item_id = Column(String(20), ForeignKey("delivery_item.delivery_item_id"), nullable=False)
    actual_quantity = Column(DECIMAL(15,3), nullable=False)
    posting_date = Column(Date, nullable=False)
    goods_issue_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    warehouse = Column(String(20))

    delivery_item = relationship("DeliveryItem", back_populates="goods_issues")
