from sqlalchemy import Column, String, DECIMAL, Text, Date
from app.models.base import Base

class Material(Base):
    __tablename__ = "material"

    material_id = Column(String(20), primary_key=True)
    material_name = Column(String(100), nullable=False)
    description = Column(Text)
    base_unit = Column(String(10), nullable=False, comment="基本计量单位")
    standard_price = Column(DECIMAL(15,2), comment="标准价格")
    weight = Column(DECIMAL(15,3), comment="重量")
    volume = Column(DECIMAL(15,3), comment="体积")
    search_term = Column(String(50))
    category = Column(String(50), comment="产品类别")
    stock_quantity = Column(DECIMAL(15,3), default=0, comment="库存数量")
    item_group = Column(String(20), comment="产品组")
    status = Column(String(10), default="ACTIVE", comment="状态")


class PricingCondition(Base):
    __tablename__ = "pricing_condition"

    condition_id = Column(String(20), primary_key=True)
    condition_type = Column(String(10), nullable=False, comment="条件类型")
    condition_name = Column(String(50), nullable=False, comment="条件名称")
    material_id = Column(String(20), comment="物料ID")
    bp_id = Column(String(20), comment="客户ID")
    amount = Column(DECIMAL(15,2), comment="金额")
    rate = Column(DECIMAL(5,2), comment="百分比/折扣率")
    currency = Column(String(3), default="CNY")
    valid_from = Column(Date)
    valid_to = Column(Date)
    status = Column(String(10), default="ACTIVE")


class SalesOrganization(Base):
    __tablename__ = "sales_organization"

    sales_org_id = Column(String(10), primary_key=True)
    description = Column(String(100), nullable=False)
    distribution_channel = Column(String(10), primary_key=True)
    division = Column(String(10), primary_key=True)
    currency = Column(String(3), default="CNY")
    country = Column(String(3), default="CN")
    status = Column(String(10), default="ACTIVE")