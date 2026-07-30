from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

# Invoice
class InvoiceItemBase(BaseModel):
    item_no: int
    material_id: str
    quantity: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    net_price: Optional[Decimal] = None

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
    sold_to_party: Optional[str] = None
    payer: Optional[str] = None
    currency: str = "CNY"
    total_amount: Optional[Decimal] = None
    status: str = "OPEN"

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

class ClosedAccountReceivableCreate(ClosedAccountReceivableBase):
    pass

class ClosedAccountReceivable(ClosedAccountReceivableBase):
    closed_time: datetime

    class Config:
        from_attributes = True

# Receipt
class ReceiptBase(BaseModel):
    receipt_id: str
    invoice_id: str
    payer: str
    receipt_amount: Decimal
    payment_method: Optional[str] = None
    currency: str = "CNY"
    reference_no: Optional[str] = None

class ReceiptCreate(ReceiptBase):
    pass

class Receipt(ReceiptBase):
    receipt_date: datetime

    class Config:
        from_attributes = True
