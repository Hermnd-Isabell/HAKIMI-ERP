from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

# Inquiry
class InquiryItemBase(BaseModel):
    item_no: int
    material_id: str
    item_description: Optional[str] = None
    order_quantity: Optional[Decimal] = None
    sales_unit: Optional[str] = None
    expected_order_value: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    net_price: Optional[Decimal] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None

class InquiryItemCreate(InquiryItemBase):
    inquiry_item_id: str

class InquiryItem(InquiryItemBase):
    inquiry_item_id: str
    inquiry_id: str

    class Config:
        from_attributes = True

class InquiryBase(BaseModel):
    inquiry_id: str
    inquiry_type: str
    status: str = "OPEN"
    customer_id: str
    sold_to_party: Optional[str] = None
    ship_to_party: Optional[str] = None
    sales_area: Optional[str] = None
    customer_reference: Optional[str] = None
    customer_reference_date: Optional[date] = None
    sales_org: Optional[str] = None
    distribution_channel: Optional[str] = None
    division: Optional[str] = None
    sales_office: Optional[str] = None
    sales_group: Optional[str] = None
    requested_delivery_date: Optional[date] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    pricing_date: Optional[date] = None
    currency: str = "CNY"
    delivering_plant: Optional[str] = None
    incoterms: Optional[str] = None
    delivery_location: Optional[str] = None
    payment_terms: Optional[str] = None
    max_partial_deliveries: int = 9
    net_value: Optional[Decimal] = None
    inquiry_address: Optional[str] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None
    created_by: Optional[str] = None

class InquiryCreate(InquiryBase):
    items: List[InquiryItemCreate]

class Inquiry(InquiryBase):
    created_time: datetime
    items: List[InquiryItem]

    class Config:
        from_attributes = True

# Quotation
class QuotationItemBase(BaseModel):
    item_no: int
    material_id: str
    item_description: Optional[str] = None
    order_quantity: Optional[Decimal] = None
    sales_unit: Optional[str] = None
    expected_order_value: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    net_price: Optional[Decimal] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None

class QuotationItemCreate(QuotationItemBase):
    quotation_item_id: str

class QuotationItem(QuotationItemBase):
    quotation_item_id: str
    quotation_id: str

    class Config:
        from_attributes = True

class QuotationBase(BaseModel):
    quotation_id: str
    inquiry_id: Optional[str] = None
    quotation_type: str
    status: str = "OPEN"
    customer_id: str
    sold_to_party: Optional[str] = None
    ship_to_party: Optional[str] = None
    sales_area: Optional[str] = None
    customer_reference: Optional[str] = None
    customer_reference_date: Optional[date] = None
    sales_org: Optional[str] = None
    distribution_channel: Optional[str] = None
    division: Optional[str] = None
    sales_office: Optional[str] = None
    sales_group: Optional[str] = None
    requested_delivery_date: Optional[date] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    pricing_date: Optional[date] = None
    currency: str = "CNY"
    payment_terms: Optional[str] = None
    incoterms: Optional[str] = None
    delivering_plant: Optional[str] = None
    max_partial_deliveries: int = 9
    net_value: Optional[Decimal] = None
    quotation_address: Optional[str] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None
    created_by: Optional[str] = None

class QuotationCreate(QuotationBase):
    items: List[QuotationItemCreate]

class Quotation(QuotationBase):
    created_time: datetime
    items: List[QuotationItem]

    class Config:
        from_attributes = True

# Sales Order
class SalesOrderItemBase(BaseModel):
    item_no: int
    material_id: str
    item_description: Optional[str] = None
    item_category: Optional[str] = None
    order_quantity: Optional[Decimal] = None
    confirmed_quantity: Optional[Decimal] = None
    sales_unit: Optional[str] = None
    plant: Optional[str] = None
    storage_location: Optional[str] = None
    shipping_point: Optional[str] = None
    unit_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    net_price: Optional[Decimal] = None
    availability_status: Optional[str] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None

class SalesOrderItemCreate(SalesOrderItemBase):
    so_item_id: str

class SalesOrderItem(SalesOrderItemBase):
    so_item_id: str
    sales_order_id: str

    class Config:
        from_attributes = True

class SalesOrderBase(BaseModel):
    sales_order_id: str
    quotation_id: Optional[str] = None
    order_type: str
    reference_type: Optional[str] = None
    reference_document: Optional[str] = None
    status: str = "OPEN"
    customer_id: str
    sold_to_party: Optional[str] = None
    ship_to_party: Optional[str] = None
    customer_reference: Optional[str] = None
    customer_reference_date: Optional[date] = None
    sales_org: Optional[str] = None
    distribution_channel: Optional[str] = None
    division: Optional[str] = None
    sales_office: Optional[str] = None
    sales_group: Optional[str] = None
    requested_delivery_date: Optional[date] = None
    pricing_date: Optional[date] = None
    currency: str = "CNY"
    payment_terms: Optional[str] = None
    incoterms: Optional[str] = None
    delivering_plant: Optional[str] = None
    shipping_condition: Optional[str] = None
    delivery_priority: Optional[str] = None
    billing_block: Optional[str] = None
    delivery_block: Optional[str] = None
    max_partial_deliveries: int = 9
    net_value: Optional[Decimal] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None
    created_by: Optional[str] = None

class SalesOrderCreate(SalesOrderBase):
    items: List[SalesOrderItemCreate]

class SalesOrder(SalesOrderBase):
    created_time: datetime
    items: List[SalesOrderItem]

    class Config:
        from_attributes = True
