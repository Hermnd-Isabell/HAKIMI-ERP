from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Integer, DECIMAL, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class BusinessPartner(Base):
    __tablename__ = "business_partner"

    bp_id = Column(String(20), primary_key=True, comment="业务伙伴唯一标识码")
    bp_type = Column(String(10), nullable=False, comment="伙伴类型: 组织/个人/公司")
    bp_role = Column(String(20), nullable=False, comment="角色: SOLD_TO/SHIP_TO/PAYER")
    bp_name = Column(String(100), nullable=False, comment="客户/公司/个人名称")
    country = Column(String(3), default="CN", comment="所属国家代码")
    city = Column(String(50), comment="所在城市")
    district = Column(String(50), comment="所在区县")
    street = Column(String(100), comment="街道地址")
    house_number = Column(String(20), comment="门牌号码")
    postal_code = Column(String(20), comment="邮政编码")
    language = Column(String(3), default="ZH", comment="通信语言")
    time_zone = Column(String(10), default="UTC+8", comment="所在时区")
    transportation_zone = Column(String(20), comment="运输区域代码")
    telephone = Column(String(20), comment="固定联系电话")
    mobile_phone = Column(String(20), comment="手机号码")
    fax = Column(String(20), comment="传真号码")
    email = Column(String(100), comment="电子邮箱地址")
    status = Column(String(20), default="ACTIVE", comment="交易状态: ACTIVE/BLOCK/ARCHIVED")
    block_reason = Column(String(255), comment="冻结或禁止交易时填写的原因")
    data_source = Column(String(20), default="MANUAL", comment="数据来源")
    print_format = Column(String(50), comment="单据默认打印格式")
    search_term = Column(String(50), comment="辅助检索用关键词")
    created_time = Column(DateTime, default=datetime.utcnow, comment="记录创建时间")
    last_changed_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="最后修改时间")

    sales_data = relationship("CustomerSalesData", back_populates="partner")
    finance_data = relationship("CustomerFinanceData", back_populates="partner")
    contacts = relationship("Contact", back_populates="partner")

class CustomerSalesData(Base):
    __tablename__ = "customer_sales_data"

    bp_id = Column(String(20), ForeignKey("business_partner.bp_id"), primary_key=True)
    sales_org = Column(String(10), primary_key=True, comment="销售组织代码")
    distribution_channel = Column(String(10), primary_key=True, comment="分销渠道代码")
    division = Column(String(10), primary_key=True, comment="产品组/事业部代码")
    sales_office = Column(String(10))
    sales_group = Column(String(10))
    sales_district = Column(String(10))
    currency = Column(String(3), default="CNY", comment="交易货币")
    price_group = Column(String(10))
    customer_pricing_procedure = Column(String(20))
    delivery_priority = Column(String(2))
    shipping_condition = Column(String(10))
    delivering_plant = Column(String(20))
    max_partial_deliveries = Column(Integer, default=9)
    incoterms = Column(String(5))
    account_assignment_group = Column(String(20))
    tax_classification = Column(String(20))

    partner = relationship("BusinessPartner", back_populates="sales_data")

class CustomerFinanceData(Base):
    __tablename__ = "customer_finance_data"

    bp_id = Column(String(20), ForeignKey("business_partner.bp_id"), primary_key=True)
    company_code = Column(String(10), primary_key=True, comment="公司代码")
    reconciliation_account = Column(String(20), comment="统驭科目")
    sort_key = Column(String(10))
    payment_terms = Column(String(10), comment="付款条件")
    bank_account_name = Column(String(100))
    bank_country = Column(String(2))
    bank_key = Column(String(20))
    bank_account = Column(String(50))
    iban = Column(String(50))
    bank_account_status = Column(String(20), default="ACTIVE")
    card_type = Column(String(10))
    card_number = Column(String(20))
    preferred_card = Column(Boolean, default=False)

    partner = relationship("BusinessPartner", back_populates="finance_data")

class Contact(Base):
    __tablename__ = "contact"

    contact_id = Column(String(20), primary_key=True)
    bp_id = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    contact_type = Column(String(20))
    contact_role = Column(String(20))
    first_name = Column(String(50))
    last_name = Column(String(50))
    department = Column(String(50))
    position = Column(String(50))
    personal_phone = Column(String(20))
    email = Column(String(100))
    status = Column(String(10), default="ACTIVE")

    partner = relationship("BusinessPartner", back_populates="contacts")

class BPRelationship(Base):
    __tablename__ = "bp_relationship"

    relation_id = Column(String(20), primary_key=True)
    relationship_type = Column(String(20), nullable=False, comment="关系类型")
    bp_from = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    bp_to = Column(String(20), ForeignKey("business_partner.bp_id"), nullable=False)
    valid_from = Column(Date)
    valid_to = Column(Date)
