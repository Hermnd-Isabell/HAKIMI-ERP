import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.core.database import SessionLocal
from app.models.material import PricingCondition, SalesOrganization
from datetime import date, timedelta
from decimal import Decimal
from app.core.config import settings

print(f"Connecting to {settings.DB_USER}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}...")

db = SessionLocal()

try:
    # 1. Sales Organizations
    orgs = [
        {"sales_org_id": "1000", "description": "Domestic Sales China", "distribution_channel": "10", "division": "01", "currency": "CNY", "country": "CN"},
        {"sales_org_id": "1000", "description": "Domestic Sales China", "distribution_channel": "10", "division": "02", "currency": "CNY", "country": "CN"},
        {"sales_org_id": "1000", "description": "Online Sales China", "distribution_channel": "20", "division": "01", "currency": "CNY", "country": "CN"},
        {"sales_org_id": "2000", "description": "Export Sales International", "distribution_channel": "10", "division": "01", "currency": "USD", "country": "US"},
        {"sales_org_id": "3000", "description": "Service Sales", "distribution_channel": "10", "division": "01", "currency": "CNY", "country": "CN"},
    ]
    
    for o in orgs:
        exists = db.query(SalesOrganization).filter_by(
            sales_org_id=o["sales_org_id"], 
            distribution_channel=o["distribution_channel"], 
            division=o["division"]
        ).first()
        if not exists:
            db.add(SalesOrganization(**o))
    
    # 2. Pricing Conditions
    today = date.today()
    conds = [
        {"condition_id": "PR0001", "condition_type": "PR00", "condition_name": "Base Price", "material_id": "MAT0001", "amount": Decimal("30.00"), "valid_from": today, "valid_to": today + timedelta(days=365)},
        {"condition_id": "PR0002", "condition_type": "PR00", "condition_name": "Base Price", "material_id": "MAT0002", "amount": Decimal("190.00"), "valid_from": today, "valid_to": today + timedelta(days=365)},
        {"condition_id": "K0071", "condition_type": "K007", "condition_name": "Customer Discount", "bp_id": "BP00001", "rate": Decimal("5.00"), "valid_from": today, "valid_to": today + timedelta(days=365)},
        {"condition_id": "K0072", "condition_type": "K007", "condition_name": "Customer Discount", "bp_id": "BP00002", "rate": Decimal("3.50"), "valid_from": today, "valid_to": today + timedelta(days=365)},
        {"condition_id": "RA001", "condition_type": "RA00", "condition_name": "Quantity Discount", "material_id": "MAT0003", "rate": Decimal("2.00"), "valid_from": today, "valid_to": today + timedelta(days=180)},
    ]
    
    for c in conds:
        exists = db.query(PricingCondition).filter_by(condition_id=c["condition_id"]).first()
        if not exists:
            db.add(PricingCondition(**c))
            
    db.commit()
    print("Successfully seeded Sales Organizations and Pricing Conditions.")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()
