import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Add the project root to sys.path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from sqlalchemy import text
from app.models.material import Material, PricingCondition, SalesOrganization
from app.models.customer import BusinessPartner, CustomerSalesData, CustomerFinanceData, Contact
from app.models.auth import User
from app.models.sales import Inquiry, InquiryItem, Quotation, QuotationItem, SalesOrder, SalesOrderItem
from app.models.logistics import Delivery, DeliveryItem, StorageLocation, GoodsIssue, PickRecord
from app.models.finance import Invoice, InvoiceItem, OpenAccountReceivable, ClosedAccountReceivable, Receipt
from app.services.auth_service import auth_service

def clear_data(db):
    print("Clearing existing data...")
    # Using raw SQL to truncate tables while disabling foreign key checks
    db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    tables = [
        "sys_user_session", "sys_user",
        "receipt", "closed_account_receivable", "open_account_receivable", 
        "invoice_item", "invoice", "pick_record", "goods_issue", 
        "delivery_item", "delivery", "sales_order_item", "sales_order", 
        "quotation_item", "quotation", "inquiry_item", "inquiry", 
        "bp_relationship", "contact", "customer_finance_data", 
        "customer_sales_data", "pricing_condition", "sales_organization", 
        "material", "business_partner", "storage_location"
    ]
    for table in tables:
        db.execute(text(f"TRUNCATE TABLE `{table}`;"))
    db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    db.commit()
    print("Data cleared.")

def seed_data(db):
    print("Seeding new test data...")
    
    # 1. Business Partners
    bp1 = BusinessPartner(
        bp_id="BP001", bp_type="ORG", bp_role="SOLD_TO", bp_name="Tech Solutions Ltd",
        country="CN", city="Shanghai", street="Pudong Road", status="ACTIVE", search_term="TECH"
    )
    bp2 = BusinessPartner(
        bp_id="BP002", bp_type="ORG", bp_role="SOLD_TO", bp_name="Global Trading Co",
        country="CN", city="Beijing", street="Changan Ave", status="ACTIVE", search_term="GLOBAL"
    )
    bp3 = BusinessPartner(
        bp_id="BP003", bp_type="ORG", bp_role="SHIP_TO", bp_name="Logistics Hub East",
        country="CN", city="Suzhou", street="Industrial Park", status="ACTIVE", search_term="HUB"
    )
    db.add_all([bp1, bp2, bp3])
    db.flush()

    # 1.1 Pricing Conditions
    pc1 = PricingCondition(
        condition_id="PR00-001", condition_type="PR00", condition_name="Base Price",
        material_id="MAT-001", amount=Decimal("5500.00"), currency="CNY", status="ACTIVE"
    )
    pc2 = PricingCondition(
        condition_id="PR00-002", condition_type="PR00", condition_name="Base Price",
        material_id="MAT-002", amount=Decimal("1200.00"), currency="CNY", status="ACTIVE"
    )
    pc3 = PricingCondition(
        condition_id="PR00-003", condition_type="PR00", condition_name="Base Price",
        material_id="MAT-003", amount=Decimal("45.00"), currency="CNY", status="ACTIVE"
    )
    db.add_all([pc1, pc2, pc3])
    db.flush()

    # 2. Materials
    m_extra = Material(
        material_id="M899071", material_name="Legacy Storage Unit", 
        description="Old model storage component", 
        base_unit="PC", standard_price=Decimal("850.00"), stock_quantity=Decimal("999999.000"),
        category="Hardware", status="ACTIVE"
    )
    db.add(m_extra)
    
    m1 = Material(
        material_id="MAT-001", material_name="Server Rack 42U", 
        description="Standard 42U server rack with cooling", 
        base_unit="PC", standard_price=Decimal("5500.00"), stock_quantity=Decimal("999999.000"),
        category="Hardware", status="ACTIVE"
    )
    m2 = Material(
        material_id="MAT-002", material_name="Network Switch 48P", 
        description="L3 Managed 48-port Gigabit Switch", 
        base_unit="PC", standard_price=Decimal("1200.00"), stock_quantity=Decimal("999999.000"),
        category="Networking", status="ACTIVE"
    )
    m3 = Material(
        material_id="MAT-003", material_name="Fiber Cable 10m", 
        description="Multimode LC-LC Fiber Patch Cord", 
        base_unit="PC", standard_price=Decimal("45.00"), stock_quantity=Decimal("999999.000"),
        category="Cabling", status="ACTIVE"
    )
    db.add_all([m1, m2, m3])
    db.flush()

    # 3. Sales Organizations
    so1 = SalesOrganization(
        sales_org_id="1000", description="Domestic Sales China", 
        distribution_channel="10", division="00", currency="CNY", country="CN"
    )
    so2 = SalesOrganization(
        sales_org_id="2000", description="Export Sales Asia", 
        distribution_channel="20", division="00", currency="USD", country="CN"
    )
    db.add_all([so1, so2])
    db.flush()

    # 4. Storage Locations
    sl1 = StorageLocation(sloc_id="WH01", sloc_name="Main Warehouse", plant="P001", storage_type="FERT")
    sl2 = StorageLocation(sloc_id="WH02", sloc_name="Express Bin", plant="P001", storage_type="PICK")
    db.add_all([sl1, sl2])
    db.flush()

    # 5. Inquiry (Status: OPEN)
    inq1 = Inquiry(
        inquiry_id="INQ260809001", inquiry_type="IN", status="OPEN",
        customer_id="BP001", sales_org="1000", distribution_channel="10", division="00",
        net_value=Decimal("15000.00"), created_time=datetime.now() - timedelta(days=5)
    )
    db.add(inq1)
    db.flush()
    db.add(InquiryItem(
        inquiry_item_id="INQITEM001", inquiry_id=inq1.inquiry_id, item_no=10,
        material_id="MAT-001", order_quantity=Decimal("2"), unit_price=Decimal("5500.00"), net_price=Decimal("11000.00")
    ))

    # 6. Quotation (Status: OPEN, linked to an Inquiry)
    quo1 = Quotation(
        quotation_id="QUO260809001", inquiry_id=inq1.inquiry_id, quotation_type="QT", status="OPEN",
        customer_id="BP001", net_value=Decimal("14500.00"), valid_to=datetime.now().date() + timedelta(days=30)
    )
    db.add(quo1)
    db.flush()
    db.add(QuotationItem(
        quotation_item_id="QUOITEM001", quotation_id=quo1.quotation_id, item_no=10,
        material_id="MAT-001", order_quantity=Decimal("2"), unit_price=Decimal("5400.00"), net_price=Decimal("10800.00")
    ))

    # 7. Sales Orders (Multiple stages)
    # SO1: OPEN
    so_open = SalesOrder(
        sales_order_id="SO260809001", order_type="OR", status="OPEN",
        customer_id="BP001", net_value=Decimal("6700.00"), created_time=datetime.now() - timedelta(days=2)
    )
    # SO2: IN_PROCESS
    so_proc = SalesOrder(
        sales_order_id="SO260809002", order_type="OR", status="IN_PROCESS",
        customer_id="BP002", net_value=Decimal("12000.00"), created_time=datetime.now() - timedelta(days=3)
    )
    db.add_all([so_open, so_proc])
    db.flush()
    
    db.add(SalesOrderItem(
        so_item_id="SOITEM001", sales_order_id=so_open.sales_order_id, item_no=10,
        material_id="MAT-001", order_quantity=Decimal("1"), unit_price=Decimal("5500.00"), net_price=Decimal("5500.00")
    ))
    db.add(SalesOrderItem(
        so_item_id="SOITEM002", sales_order_id=so_proc.sales_order_id, item_no=10,
        material_id="MAT-002", order_quantity=Decimal("10"), unit_price=Decimal("1200.00"), net_price=Decimal("12000.00")
    ))

    # 8. Deliveries (Multiple stages)
    # DEL1: OPEN (Ready for Picking)
    del_open = Delivery(
        delivery_id="DEL260809001", sales_order_id=so_proc.sales_order_id,
        delivery_type="LF", delivery_status="OPEN", ship_to_party="BP003",
        planned_gi_date=datetime.now().date(), created_time=datetime.now() - timedelta(hours=5)
    )
    # DEL2: IN_TRANSIT
    del_transit = Delivery(
        delivery_id="DEL260809002", sales_order_id=so_proc.sales_order_id,
        delivery_type="LF", delivery_status="IN_TRANSIT", ship_to_party="BP003",
        actual_gi_date=datetime.now() - timedelta(days=1), created_time=datetime.now() - timedelta(days=1)
    )
    # DEL3: PGI_DONE
    del_done = Delivery(
        delivery_id="DEL260809003", sales_order_id=so_proc.sales_order_id,
        delivery_type="LF", delivery_status="PGI_DONE", ship_to_party="BP003",
        actual_gi_date=datetime.now() - timedelta(days=2), created_time=datetime.now() - timedelta(days=2)
    )
    db.add_all([del_open, del_transit, del_done])
    db.flush()

    db.add(DeliveryItem(
        delivery_item_id="DITEM001", delivery_id=del_open.delivery_id, item_no=10,
        material_id="MAT-002", order_quantity=Decimal("5"), delivery_quantity=Decimal("5"), picked_quantity=Decimal("0")
    ))
    db.add(DeliveryItem(
        delivery_item_id="DITEM002", delivery_id=del_transit.delivery_id, item_no=10,
        material_id="MAT-002", order_quantity=Decimal("3"), delivery_quantity=Decimal("3"), picked_quantity=Decimal("3")
    ))
    db.add(DeliveryItem(
        delivery_item_id="DITEM003", delivery_id=del_done.delivery_id, item_no=10,
        material_id="MAT-002", order_quantity=Decimal("2"), delivery_quantity=Decimal("2"), picked_quantity=Decimal("2")
    ))

    # 9. Invoices
    inv1 = Invoice(
        invoice_id="INV260809001", delivery_id=del_done.delivery_id, sales_order_id=so_proc.sales_order_id,
        billing_type="F2", invoice_date=datetime.now().date(), billing_date=datetime.now().date(),
        sold_to_party="BP002", payer="BP002", total_amount=Decimal("2400.00"), status="OPEN"
    )
    db.add(inv1)
    db.flush()

    db.add(InvoiceItem(
        invoice_item_id="INVITEM001", invoice_id=inv1.invoice_id, item_no=10,
        material_id="MAT-002", quantity=Decimal("2"), unit_price=Decimal("1200.00"), net_price=Decimal("2400.00")
    ))

    # 10. Account Receivables
    ar1 = OpenAccountReceivable(
        open_ar_id="AR260809001", invoice_id=inv1.invoice_id,
        receivable_amount=Decimal("2400.00"), received_amount=Decimal("0.00"),
        due_date=datetime.now().date() + timedelta(days=30), status="UNPAID",
        created_time=datetime.now()
    )
    db.add(ar1)

    db.add(User(
        username="admin",
        email="admin@hakimi-erp.local",
        password_hash=auth_service.hash_password("admin123"),
        full_name="System Administrator",
        role="ADMIN",
        is_active=True,
    ))

    db.commit()
    print("Seed data inserted successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        clear_data(db)
        seed_data(db)
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
