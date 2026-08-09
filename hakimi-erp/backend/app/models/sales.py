from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Integer, DECIMAL, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Inquiry(Base):
    __tablename__ = "inquiry"

    inquiry_id = Column(String(20), primary_key=True)
    inquiry_type = Column(String(20), nullable=False)
    status = Column(String(20), default="OPEN", comment="OPEN/CLOSED/CANCELLED")
    customer_id = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    sold_to_party = Column(String(20))
    ship_to_party = Column(String(20))
    sales_area = Column(String(100))
    customer_reference = Column(String(50))
    customer_reference_date = Column(Date)
    sales_org = Column(String(10))
    distribution_channel = Column(String(10))
    division = Column(String(10))
    sales_office = Column(String(10))
    sales_group = Column(String(10))
    requested_delivery_date = Column(Date)
    valid_from = Column(Date)
    valid_to = Column(Date)
    pricing_date = Column(Date)
    currency = Column(String(3), default="CNY")
    delivering_plant = Column(String(20))
    incoterms = Column(String(5))
    delivery_location = Column(String(100))
    payment_terms = Column(String(10))
    max_partial_deliveries = Column(Integer, default=9)
    net_value = Column(DECIMAL(15,2))
    inquiry_address = Column(String(255))
    remark = Column(Text)
    search_term = Column(String(20))
    created_time = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(20))

    items = relationship("InquiryItem", back_populates="inquiry", cascade="all, delete-orphan")

class InquiryItem(Base):
    __tablename__ = "inquiry_item"

    inquiry_item_id = Column(String(20), primary_key=True)
    inquiry_id = Column(String(20), ForeignKey("inquiry.inquiry_id"), nullable=False)
    item_no = Column(Integer, nullable=False, comment="行号: 10, 20, 30...")
    material_id = Column(String(20), ForeignKey("material.material_id"), nullable=False)
    item_description = Column(String(255))
    order_quantity = Column(DECIMAL(15,3))
    sales_unit = Column(String(10))
    expected_order_value = Column(DECIMAL(15,2))
    unit_price = Column(DECIMAL(15,2))
    discount = Column(DECIMAL(15,2))
    net_price = Column(DECIMAL(15,2))
    remark = Column(Text)
    search_term = Column(String(20))

    __table_args__ = (UniqueConstraint('inquiry_id', 'item_no', name='uk_inquiry_item'),)

    inquiry = relationship("Inquiry", back_populates="items")

class Quotation(Base):
    __tablename__ = "quotation"

    quotation_id = Column(String(20), primary_key=True)
    inquiry_id = Column(String(20), ForeignKey("inquiry.inquiry_id"))
    quotation_type = Column(String(20), nullable=False)
    status = Column(String(20), default="OPEN")
    customer_id = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    sold_to_party = Column(String(20))
    ship_to_party = Column(String(20))
    sales_area = Column(String(100))
    customer_reference = Column(String(50))
    customer_reference_date = Column(Date)
    sales_org = Column(String(10))
    distribution_channel = Column(String(10))
    division = Column(String(10))
    sales_office = Column(String(10))
    sales_group = Column(String(10))
    requested_delivery_date = Column(Date)
    valid_from = Column(Date)
    valid_to = Column(Date)
    pricing_date = Column(Date)
    currency = Column(String(3), default="CNY")
    payment_terms = Column(String(10))
    incoterms = Column(String(5))
    delivering_plant = Column(String(20))
    max_partial_deliveries = Column(Integer, default=9)
    net_value = Column(DECIMAL(15,2))
    quotation_address = Column(String(255))
    remark = Column(Text)
    search_term = Column(String(20))
    created_time = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(20))

    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")

class QuotationItem(Base):
    __tablename__ = "quotation_item"

    quotation_item_id = Column(String(20), primary_key=True)
    quotation_id = Column(String(20), ForeignKey("quotation.quotation_id"), nullable=False)
    item_no = Column(Integer, nullable=False)
    material_id = Column(String(20), ForeignKey("material.material_id"), nullable=False)
    item_description = Column(String(255))
    order_quantity = Column(DECIMAL(15,3))
    sales_unit = Column(String(10))
    expected_order_value = Column(DECIMAL(15,2))
    unit_price = Column(DECIMAL(15,2))
    discount = Column(DECIMAL(15,2))
    net_price = Column(DECIMAL(15,2))
    remark = Column(Text)
    search_term = Column(String(20))

    __table_args__ = (UniqueConstraint('quotation_id', 'item_no', name='uk_quotation_item'),)

    quotation = relationship("Quotation", back_populates="items")

class SalesOrder(Base):
    __tablename__ = "sales_order"

    sales_order_id = Column(String(20), primary_key=True)
    quotation_id = Column(String(20), ForeignKey("quotation.quotation_id"))
    order_type = Column(String(20), nullable=False)
    reference_type = Column(String(1))
    reference_document = Column(String(20))
    status = Column(String(20), default="OPEN")
    customer_id = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    sold_to_party = Column(String(20))
    ship_to_party = Column(String(20))
    customer_reference = Column(String(50))
    customer_reference_date = Column(Date)
    sales_org = Column(String(10))
    distribution_channel = Column(String(10))
    division = Column(String(10))
    sales_office = Column(String(10))
    sales_group = Column(String(10))
    requested_delivery_date = Column(Date)
    pricing_date = Column(Date)
    currency = Column(String(3), default="CNY")
    payment_terms = Column(String(10))
    incoterms = Column(String(5))
    delivering_plant = Column(String(20))
    shipping_condition = Column(String(10))
    delivery_priority = Column(String(2))
    billing_block = Column(String(20))
    delivery_block = Column(String(20))
    max_partial_deliveries = Column(Integer, default=9)
    net_value = Column(DECIMAL(15,2))
    remark = Column(Text)
    search_term = Column(String(20))
    created_time = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(20))

    items = relationship("SalesOrderItem", back_populates="order", cascade="all, delete-orphan")

class SalesOrderItem(Base):
    __tablename__ = "sales_order_item"

    so_item_id = Column(String(20), primary_key=True)
    sales_order_id = Column(String(20), ForeignKey("sales_order.sales_order_id"), nullable=False)
    item_no = Column(Integer, nullable=False)
    material_id = Column(String(20), ForeignKey("material.material_id"), nullable=False)
    item_description = Column(String(255))
    item_category = Column(String(10))
    order_quantity = Column(DECIMAL(15,3))
    confirmed_quantity = Column(DECIMAL(15,3))
    sales_unit = Column(String(10))
    plant = Column(String(20))
    storage_location = Column(String(10))
    shipping_point = Column(String(10))
    unit_price = Column(DECIMAL(15,2))
    discount = Column(DECIMAL(15,2))
    net_price = Column(DECIMAL(15,2))
    availability_status = Column(String(20))
    remark = Column(Text)
    search_term = Column(String(20))

    __table_args__ = (UniqueConstraint('sales_order_id', 'item_no', name='uk_sales_order_item'),)

    order = relationship("SalesOrder", back_populates="items")
