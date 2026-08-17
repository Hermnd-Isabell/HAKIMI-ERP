"""Debug AR open/closed 500 error"""
import sys
sys.path.insert(0, r"E:\Tongji University\2026SDsystem\HAKIMI-ERP\hakimi-erp\backend")

from app.core.database import SessionLocal
from app.services.finance_service import finance_service

db = SessionLocal()

print("=== Testing get_open_ar ===")
try:
    items, total = finance_service.get_open_ar(db, skip=0, limit=20)
    print(f"OK: total={total}, items={len(items)}")
    for item in items:
        print(f"  invoice_id={item.invoice_id}, status={item.status}")
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n=== Testing get_closed_ar ===")
try:
    items, total = finance_service.get_closed_ar(db, skip=0, limit=20)
    print(f"OK: total={total}, items={len(items)}")
    for item in items:
        print(f"  invoice_id={item.invoice_id}")
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n=== Testing get_receipts (used by closed AR endpoint) ===")
try:
    items, total = finance_service.get_receipts(db, skip=0, limit=20)
    print(f"OK: total={total}, items={len(items)}")
except Exception as e:
    import traceback
    traceback.print_exc()

db.close()
