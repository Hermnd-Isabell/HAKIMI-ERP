from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Integer, DECIMAL, Text, UniqueConstraint
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
    sales_org = Column(String(4), comment="销售组织代码")
    distribution_channel = Column(String(2), comment="分销渠道代码")
    division = Column(String(2), comment="产品组/事业部代码")
    shipping_point = Column(String(20), comment="装运点/发货点")
    sold_to_party = Column(String(20))
    payer = Column(String(20), ForeignKey("business_partner.bp_id"))
    destination_country = Column(String(3), comment="货物目的国家")
    currency = Column(String(3), default="CNY")
    total_amount = Column(DECIMAL(15,2))
    status = Column(String(20), nullable=False, default="OPEN", comment="OPEN/PARTIAL/CLEARED/VOID")
    remark = Column(Text, comment="其他补充说明")
    search_term = Column(String(50), comment="辅助检索用关键词")

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
    sales_unit = Column(String(10), comment="销售计量单位")
    unit_price = Column(DECIMAL(15,2))
    discount = Column(DECIMAL(5,2), comment="折扣百分比或金额")
    tax_amount = Column(DECIMAL(15,2))
    net_price = Column(DECIMAL(15,2))
    item_description = Column(String(500), comment="行项目补充说明")
    remark = Column(Text, comment="其他补充说明")

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
    remark = Column(Text, comment="其他补充说明")
    search_term = Column(String(50), comment="辅助检索用关键词")
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
    remark = Column(Text, comment="其他补充说明")
    search_term = Column(String(50), comment="辅助检索用关键词")

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
    remark = Column(Text, comment="其他补充说明")
    search_term = Column(String(50), comment="辅助检索用关键词")

    invoice = relationship("Invoice", back_populates="receipts")
