from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Integer, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Delivery(Base):
    __tablename__ = "delivery"

    delivery_id = Column(String(20), primary_key=True)
    sales_order_id = Column(String(20), ForeignKey("sales_order.sales_order_id"))
    delivery_type = Column(String(20), nullable=False)
    delivery_status = Column(String(20), nullable=False, comment="OPEN/PICKING/SHIPPED/IN_TRANSIT/PGI_DONE/CANCELLED")
    ship_to_party = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    planned_delivery_date = Column(Date)
    planned_gi_date = Column(Date)
    actual_gi_date = Column(DateTime)
    picking_date = Column(Date)
    shipping_point = Column(String(20))
    carrier = Column(String(100))
    driver_name = Column(String(50))
    route = Column(String(100))
    tracking_no = Column(String(50))

    items = relationship("DeliveryItem", back_populates="delivery", cascade="all, delete-orphan")
    ship_to = relationship("BusinessPartner", foreign_keys=[ship_to_party], lazy="joined")

class DeliveryItem(Base):
    __tablename__ = "delivery_item"

    delivery_item_id = Column(String(20), primary_key=True)
    delivery_id = Column(String(20), ForeignKey("delivery.delivery_id"), nullable=False)
    item_no = Column(Integer, nullable=False)
    so_item_id = Column(String(20), ForeignKey("sales_order_item.so_item_id"))
    material_id = Column(String(20), ForeignKey("material.material_id"), nullable=False)
    order_quantity = Column(DECIMAL(15,3), default=0)
    delivery_quantity = Column(DECIMAL(15,3))
    picked_quantity = Column(DECIMAL(15,3), default=0)
    sales_unit = Column(String(10))
    plant = Column(String(20))
    storage_location = Column(String(10))
    item_description = Column(String(255))
    item_status = Column(String(20), default="OPEN")

    __table_args__ = (UniqueConstraint('delivery_id', 'item_no', name='uk_delivery_item'),)

    delivery = relationship("Delivery", back_populates="items")
    material = relationship("Material", foreign_keys=[material_id], lazy="joined")
    goods_issues = relationship("GoodsIssue", back_populates="delivery_item")
    pick_records = relationship("PickRecord", back_populates="delivery_item", order_by="PickRecord.batch_no")

class GoodsIssue(Base):
    __tablename__ = "goods_issue"

    goods_issue_id = Column(String(20), primary_key=True)
    delivery_item_id = Column(String(20), ForeignKey("delivery_item.delivery_item_id"), nullable=False)
    actual_quantity = Column(DECIMAL(15,3), nullable=False)
    posting_date = Column(Date, nullable=False)
    goods_issue_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    warehouse = Column(String(20))
    batch_no = Column(Integer, default=1)

    delivery_item = relationship("DeliveryItem", back_populates="goods_issues")

class PickRecord(Base):
    __tablename__ = "pick_record"

    pick_id = Column(String(20), primary_key=True)
    delivery_item_id = Column(String(20), ForeignKey("delivery_item.delivery_item_id"), nullable=False)
    batch_no = Column(Integer, nullable=False)
    pick_quantity = Column(DECIMAL(15,3), nullable=False, default=0)
    storage_location = Column(String(10))
    pick_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    picked_by = Column(String(50))

    delivery_item = relationship("DeliveryItem", back_populates="pick_records")


class StorageLocation(Base):
    __tablename__ = "storage_location"

    sloc_id = Column(String(10), primary_key=True)
    sloc_name = Column(String(100), nullable=False)
    plant = Column(String(20), nullable=False)
    warehouse_no = Column(String(10))
    storage_type = Column(String(20))
    storage_bin = Column(String(20))
    description = Column(String(255))
