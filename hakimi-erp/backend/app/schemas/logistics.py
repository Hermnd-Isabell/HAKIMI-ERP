from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

# Delivery
class DeliveryItemBase(BaseModel):
    item_no: int
    so_item_id: Optional[str] = None
    material_id: str
    delivery_quantity: Optional[Decimal] = None
    sales_unit: Optional[str] = None
    item_description: Optional[str] = None

class DeliveryItemCreate(DeliveryItemBase):
    delivery_item_id: str

class DeliveryItem(DeliveryItemBase):
    delivery_item_id: str
    delivery_id: str

    class Config:
        from_attributes = True

class DeliveryBase(BaseModel):
    delivery_id: str
    sales_order_id: Optional[str] = None
    delivery_type: str
    delivery_status: str
    ship_to_party: str
    planned_delivery_date: Optional[date] = None
    planned_gi_date: Optional[date] = None
    actual_gi_date: Optional[datetime] = None
    picking_date: Optional[date] = None
    shipping_point: Optional[str] = None

class DeliveryCreate(DeliveryBase):
    items: List[DeliveryItemCreate]

class Delivery(DeliveryBase):
    items: List[DeliveryItem]

    class Config:
        from_attributes = True

# Goods Issue
class GoodsIssueBase(BaseModel):
    goods_issue_id: str
    delivery_item_id: str
    actual_quantity: Decimal
    posting_date: date
    warehouse: Optional[str] = None

class GoodsIssueCreate(GoodsIssueBase):
    pass

class GoodsIssue(GoodsIssueBase):
    goods_issue_time: datetime

    class Config:
        from_attributes = True
