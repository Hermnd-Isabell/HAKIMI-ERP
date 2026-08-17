from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

# Invoice
class InvoiceItemBase(BaseModel):
    item_no: int
    material_id: str
    quantity: Optional[Decimal] = None
    sales_unit: Optional[str] = None
    unit_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    net_price: Optional[Decimal] = None
    item_description: Optional[str] = None
    remark: Optional[str] = None

class InvoiceItemCreate(InvoiceItemBase):
    invoice_item_id: str

class InvoiceItem(InvoiceItemBase):
    invoice_item_id: str
    invoice_id: str

    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    invoice_id: str
    delivery_id: Optional[str] = None
    sales_order_id: Optional[str] = None
    billing_type: str
    invoice_date: date
    billing_date: date
    sales_org: Optional[str] = None
    distribution_channel: Optional[str] = None
    division: Optional[str] = None
    shipping_point: Optional[str] = None
    sold_to_party: Optional[str] = None
    payer: Optional[str] = None
    destination_country: Optional[str] = None
    currency: str = "CNY"
    total_amount: Optional[Decimal] = None
    status: str = "OPEN"
    remark: Optional[str] = None
    search_term: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate]

class Invoice(InvoiceBase):
    items: List[InvoiceItem]

    class Config:
        from_attributes = True

# Account Receivable
class OpenAccountReceivableBase(BaseModel):
    open_ar_id: str
    invoice_id: str
    receivable_amount: Decimal
    received_amount: Decimal = Decimal("0.00")
    due_date: Optional[date] = None
    status: str = "UNPAID"
    remark: Optional[str] = None
    search_term: Optional[str] = None

class OpenAccountReceivableCreate(OpenAccountReceivableBase):
    pass

class OpenAccountReceivable(OpenAccountReceivableBase):
    created_time: datetime

    class Config:
        from_attributes = True

class ClosedAccountReceivableBase(BaseModel):
    closed_ar_id: str
    invoice_id: str
    receivable_amount: Decimal
    received_amount: Decimal
    created_time: Optional[datetime] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None

class ClosedAccountReceivableCreate(ClosedAccountReceivableBase):
    pass

class ClosedAccountReceivable(ClosedAccountReceivableBase):
    closed_time: datetime

    class Config:
        from_attributes = True

# Receipt
# ReceiptBase 不包含 receipt_id（由后端自动生成）和 payer（由后端从发票推导）
class ReceiptBase(BaseModel):
    invoice_id: str
    receipt_amount: Decimal
    payment_method: Optional[str] = None
    currency: str = "CNY"
    reference_no: Optional[str] = None
    remark: Optional[str] = None
    search_term: Optional[str] = None

class ReceiptCreate(ReceiptBase):
    pass

class Receipt(ReceiptBase):
    receipt_id: str
    payer: str
    receipt_date: datetime

    class Config:
        from_attributes = True
