from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal

class MaterialBase(BaseModel):
    material_id: str = Field(..., max_length=20)
    material_name: str = Field(..., max_length=100)
    description: Optional[str] = None
    base_unit: str = Field(..., max_length=10)
    standard_price: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    volume: Optional[Decimal] = None
    search_term: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    material_name: Optional[str] = None
    description: Optional[str] = None
    base_unit: Optional[str] = None
    standard_price: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    volume: Optional[Decimal] = None
    search_term: Optional[str] = None

class Material(MaterialBase):
    class Config:
        from_attributes = True
