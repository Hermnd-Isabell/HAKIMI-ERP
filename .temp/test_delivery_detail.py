import sys
sys.path.insert(0, r"E:\Tongji University\2026SDsystem\HAKIMI-ERP\hakimi-erp\backend")

from app.core.database import SessionLocal
from app.services.logistics_service import logistics_service

db = SessionLocal()
try:
    result = logistics_service.get_delivery_detail(db, "DLV00001")
    print("SUCCESS")
    print(type(result))
    if result:
        for k, v in result.items():
            if k == "items":
                print(f"  items: {len(v)} items")
            else:
                print(f"  {k}: {v}")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"ERROR: {e}")
finally:
    db.close()
