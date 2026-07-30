from sqlalchemy import Column, String, DECIMAL, Text
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
