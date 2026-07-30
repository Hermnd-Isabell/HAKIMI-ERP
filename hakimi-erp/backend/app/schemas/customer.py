from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date

# Business Partner
class BusinessPartnerBase(BaseModel):
    bp_id: str = Field(..., max_length=20)
    bp_type: str = Field(..., max_length=10)
    bp_role: str = Field(..., max_length=20)
    bp_name: str = Field(..., max_length=100)
    country: Optional[str] = "CN"
    city: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    language: Optional[str] = "ZH"
    time_zone: Optional[str] = "UTC+8"
    transportation_zone: Optional[str] = None
    telephone: Optional[str] = None
    mobile_phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = "ACTIVE"
    block_reason: Optional[str] = None
    data_source: Optional[str] = "MANUAL"
    print_format: Optional[str] = None
    search_term: Optional[str] = None

class BusinessPartnerCreate(BusinessPartnerBase):
    pass

class BusinessPartnerUpdate(BaseModel):
    bp_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    telephone: Optional[str] = None
    mobile_phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    block_reason: Optional[str] = None

class BusinessPartner(BusinessPartnerBase):
    created_time: datetime
    last_changed_time: datetime

    class Config:
        from_attributes = True

# Sales Data
class CustomerSalesDataBase(BaseModel):
    sales_org: str
    distribution_channel: str
    division: str
    sales_office: Optional[str] = None
    sales_group: Optional[str] = None
    sales_district: Optional[str] = None
    currency: str = "CNY"
    price_group: Optional[str] = None
    customer_pricing_procedure: Optional[str] = None
    delivery_priority: Optional[str] = None
    shipping_condition: Optional[str] = None
    delivering_plant: Optional[str] = None
    max_partial_deliveries: int = 9
    incoterms: Optional[str] = None
    account_assignment_group: Optional[str] = None
    tax_classification: Optional[str] = None

class CustomerSalesDataCreate(CustomerSalesDataBase):
    bp_id: str

class CustomerSalesData(CustomerSalesDataBase):
    bp_id: str

    class Config:
        from_attributes = True

# Finance Data
class CustomerFinanceDataBase(BaseModel):
    company_code: str
    reconciliation_account: Optional[str] = None
    sort_key: Optional[str] = None
    payment_terms: Optional[str] = None
    bank_account_name: Optional[str] = None
    bank_country: Optional[str] = None
    bank_key: Optional[str] = None
    bank_account: Optional[str] = None
    iban: Optional[str] = None
    bank_account_status: str = "ACTIVE"
    card_type: Optional[str] = None
    card_number: Optional[str] = None
    preferred_card: bool = False

class CustomerFinanceDataCreate(CustomerFinanceDataBase):
    bp_id: str

class CustomerFinanceData(CustomerFinanceDataBase):
    bp_id: str

    class Config:
        from_attributes = True

# Contact
class ContactBase(BaseModel):
    contact_id: str
    contact_type: Optional[str] = None
    contact_role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    personal_phone: Optional[str] = None
    email: Optional[str] = None
    status: str = "ACTIVE"

class ContactCreate(ContactBase):
    bp_id: str

class Contact(ContactBase):
    bp_id: str

    class Config:
        from_attributes = True

# Relationship
class BPRelationshipBase(BaseModel):
    relation_id: str
    relationship_type: str
    bp_from: str
    bp_to: str
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None

class BPRelationshipCreate(BPRelationshipBase):
    pass

class BPRelationship(BPRelationshipBase):
    class Config:
        from_attributes = True
