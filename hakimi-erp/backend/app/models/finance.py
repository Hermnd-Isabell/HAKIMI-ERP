from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Integer, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Invoice(Base):
    __tablename__ = "invoice"

    invoice_id = Column(String(20), primary_key=True)
    delivery_id = Column(String(20), ForeignKey("delivery.delivery_id"))
    sales_order_id = Column(String(20), ForeignKey("sales_order.sales_order_id"))
    billing_type = Column(String(20), nullable=False)
    invoice_date = Column(Date, nullable=False)
    billing_date = Column(Date, nullable=False)
    sold_to_party = Column(String(20))
    payer = Column(String(20), ForeignKey("business_partner.bp_id"))
    currency = Column(String(3), default="CNY")
    total_amount = Column(DECIMAL(15,2))
    status = Column(String(20), nullable=False, default="OPEN", comment="OPEN/PARTIAL/CLEARED/VOID")

    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    receipts = relationship("Receipt", back_populates="invoice")
    open_ar = relationship("OpenAccountReceivable", back_populates="invoice", uselist=False)
    closed_ar = relationship("ClosedAccountReceivable", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_item"

    invoice_item_id = Column(String(20), primary_key=True)
    invoice_id = Column(String(20), ForeignKey("invoice.invoice_id"), nullable=False)
    item_no = Column(Integer, nullable=False)
    material_id = Column(String(20), ForeignKey("material.material_id"), nullable=False)
    quantity = Column(DECIMAL(15,3))
    unit_price = Column(DECIMAL(15,2))
    tax_amount = Column(DECIMAL(15,2))
    net_price = Column(DECIMAL(15,2))

    __table_args__ = (UniqueConstraint('invoice_id', 'item_no', name='uk_invoice_item'),)

    invoice = relationship("Invoice", back_populates="items")

class OpenAccountReceivable(Base):
    __tablename__ = "open_account_receivable"

    open_ar_id = Column(String(20), primary_key=True)
    invoice_id = Column(String(20), ForeignKey("invoice.invoice_id"), nullable=False, unique=True)
    receivable_amount = Column(DECIMAL(15,2), nullable=False)
    received_amount = Column(DECIMAL(15,2), default=0.00)
    due_date = Column(Date)
    status = Column(String(20), default="UNPAID", comment="UNPAID/PARTIAL/OVERDUE")
    created_time = Column(DateTime, default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="open_ar")

class ClosedAccountReceivable(Base):
    __tablename__ = "closed_account_receivable"

    closed_ar_id = Column(String(20), primary_key=True)
    invoice_id = Column(String(20), ForeignKey("invoice.invoice_id"), nullable=False)
    receivable_amount = Column(DECIMAL(15,2), nullable=False)
    received_amount = Column(DECIMAL(15,2), nullable=False)
    created_time = Column(DateTime)
    closed_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    invoice = relationship("Invoice", back_populates="closed_ar")

class Receipt(Base):
    __tablename__ = "receipt"

    receipt_id = Column(String(20), primary_key=True)
    invoice_id = Column(String(20), ForeignKey("invoice.invoice_id"), nullable=False)
    payer = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    receipt_amount = Column(DECIMAL(15,2), nullable=False)
    receipt_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    payment_method = Column(String(20))
    currency = Column(String(3), default="CNY")
    reference_no = Column(String(50))

    invoice = relationship("Invoice", back_populates="receipts")
