from typing import Optional, List
from pydantic import BaseModel, model_validator
from datetime import datetime, date
from decimal import Decimal

# --- Delivery Item ---
class DeliveryItemBase(BaseModel):
    item_no: int
    so_item_id: Optional[str] = None
    material_id: str
    order_quantity: Optional[Decimal] = None
    delivery_quantity: Optional[Decimal] = None
    picked_quantity: Optional[Decimal] = None
    sales_unit: Optional[str] = None
    plant: Optional[str] = None
    storage_location: Optional[str] = None
    item_description: Optional[str] = None
    item_status: Optional[str] = "OPEN"

class DeliveryItemCreate(DeliveryItemBase):
    delivery_item_id: str

class DeliveryItem(DeliveryItemBase):
    delivery_item_id: str
    delivery_id: str
    material_name: Optional[str] = None
    base_unit: Optional[str] = None

    class Config:
        from_attributes = True

# --- Delivery ---
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
    carrier: Optional[str] = None
    driver_name: Optional[str] = None
    route: Optional[str] = None
    tracking_no: Optional[str] = None

class DeliveryCreate(DeliveryBase):
    items: List[DeliveryItemCreate]

class Delivery(DeliveryBase):
    ship_to_party_name: Optional[str] = None
    ship_to_address: Optional[str] = None
    items: List[DeliveryItem] = []
    total_quantity: Optional[Decimal] = None
    delivered_quantity: Optional[Decimal] = None

    class Config:
        from_attributes = True

# --- Delivery List Item (lightweight) ---
class DeliveryListItem(BaseModel):
    delivery_id: str
    sales_order_id: Optional[str] = None
    delivery_type: str
    delivery_status: str
    ship_to_party: str
    ship_to_party_name: Optional[str] = None
    planned_delivery_date: Optional[date] = None
    planned_gi_date: Optional[date] = None
    actual_gi_date: Optional[datetime] = None
    picking_date: Optional[date] = None
    shipping_point: Optional[str] = None
    total_quantity: Optional[Decimal] = None
    delivered_quantity: Optional[Decimal] = None

    class Config:
        from_attributes = True

# --- Goods Issue ---
class GoodsIssueBase(BaseModel):
    goods_issue_id: str
    delivery_item_id: str
    actual_quantity: Decimal
    posting_date: date
    warehouse: Optional[str] = None
    batch_no: Optional[int] = 1

class GoodsIssueCreate(GoodsIssueBase):
    pass

class GoodsIssue(GoodsIssueBase):
    goods_issue_time: datetime
    material_id: Optional[str] = None
    material_name: Optional[str] = None

    class Config:
        from_attributes = True


# --- Partial Picking / PGI request schemas ---
class PartialItemQuantity(BaseModel):
    delivery_item_id: str
    quantity: Decimal

class PartialPickingRequest(BaseModel):
    items: List[PartialItemQuantity]

class PartialPgiRequest(BaseModel):
    items: List[PartialItemQuantity]


# --- Pick Record (batch picking) ---
class PickRecordBase(BaseModel):
    pick_id: str
    delivery_item_id: str
    batch_no: int
    pick_quantity: Decimal
    storage_location: Optional[str] = None
    pick_date: datetime
    picked_by: Optional[str] = None

class PickRecord(PickRecordBase):
    material_id: Optional[str] = None
    material_name: Optional[str] = None

    class Config:
        from_attributes = True

class PickBatchRequest(BaseModel):
    items: List[PartialItemQuantity]
    storage_location: Optional[str] = None
    picked_by: Optional[str] = None

# --- SAP-style remaining quantity ---
class SoItemRemaining(BaseModel):
    so_item_id: str
    material_id: str
    material_name: Optional[str] = None
    order_quantity: Decimal
    already_delivered: Decimal
    remaining_quantity: Decimal
    sales_unit: Optional[str] = None

# --- Status mapping helpers ---
DELIVERY_STATUS_LABELS = {
    "OPEN": "Creating",
    "PICKING": "Picking",
    "SHIPPED": "Picked",
    "IN_TRANSIT": "In Transit",
    "PGI_DONE": "Completed",
    "CANCELLED": "Cancelled",
}

def get_status_label(status: str) -> str:
    return DELIVERY_STATUS_LABELS.get(status, status)

def get_status_index(status: str) -> int:
    mapping = {"OPEN": 0, "PICKING": 1, "SHIPPED": 2, "IN_TRANSIT": 3, "PGI_DONE": 4, "CANCELLED": -1}
    return mapping.get(status, 0)
