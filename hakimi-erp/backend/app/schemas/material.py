from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime, date

class MaterialBase(BaseModel):
    material_id: str
    material_name: str
    description: Optional[str] = None
    base_unit: str
    standard_price: Optional[Decimal] = None
    weight: Optional[Decimal] = None
    volume: Optional[Decimal] = None
    search_term: Optional[str] = None
    category: Optional[str] = None
    stock_quantity: Optional[Decimal] = None
    item_group: Optional[str] = None
    status: Optional[str] = None

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
    category: Optional[str] = None
    stock_quantity: Optional[Decimal] = None
    item_group: Optional[str] = None
    status: Optional[str] = None

class Material(MaterialBase):
    class Config:
        from_attributes = True


class PricingConditionBase(BaseModel):
    condition_type: str
    condition_name: str
    material_id: Optional[str] = None
    bp_id: Optional[str] = None
    amount: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    currency: Optional[str] = "CNY"
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    status: Optional[str] = "ACTIVE"

class PricingCondition(PricingConditionBase):
    condition_id: str
    class Config:
        from_attributes = True


class SalesOrganizationBase(BaseModel):
    sales_org_id: str
    description: str
    distribution_channel: str
    division: str
    currency: Optional[str] = "CNY"
    country: Optional[str] = "CN"
    status: Optional[str] = "ACTIVE"

class SalesOrganization(SalesOrganizationBase):
    class Config:
        from_attributes = True