"""Debug: test exact API serialization for AR endpoints"""
import sys
sys.path.insert(0, r"E:\Tongji University\2026SDsystem\HAKIMI-ERP\hakimi-erp\backend")

from app.core.database import SessionLocal
from app.services.finance_service import finance_service
from app.schemas.finance import OpenAccountReceivable, ClosedAccountReceivable, Receipt
from app.schemas.base import ResponseModel, PaginatedData, Pagination
import math
import json

db = SessionLocal()

print("=== Testing OpenAR serialization ===")
try:
    items, total = finance_service.get_open_ar(db, skip=0, limit=1000)
    print(f"  Service OK: {len(items)} items, total={total}")
    
    # Try Pydantic validation
    schemas = [OpenAccountReceivable.model_validate(item) for item in items]
    print(f"  Schema validation OK: {len(schemas)} items")
    for s in schemas:
        print(f"    {s.open_ar_id} | invoice={s.invoice_id} | due_date={s.due_date} | created_time={s.created_time}")
    
    # Try full ResponseModel wrapping
    total_pages = math.ceil(total / 1000) if total > 0 else 0
    pagination = Pagination(page=1, page_size=1000, total=total, total_pages=total_pages)
    paginated = PaginatedData(items=schemas, pagination=pagination)
    response = ResponseModel(data=paginated)
    json_str = response.model_dump_json()
    print(f"  JSON serialization OK, length={len(json_str)}")
    print(f"  First 500 chars: {json_str[:500]}")
    
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n=== Testing ClosedAR serialization ===")
try:
    items, total = finance_service.get_closed_ar(db, skip=0, limit=1000)
    print(f"  Service OK: {len(items)} items, total={total}")
    
    schemas = [ClosedAccountReceivable.model_validate(item) for item in items]
    print(f"  Schema validation OK: {len(schemas)} items")
    for s in schemas:
        print(f"    {s.closed_ar_id} | invoice={s.invoice_id} | closed_time={s.closed_time} | created_time={s.created_time}")
    
    total_pages = math.ceil(total / 1000) if total > 0 else 0
    pagination = Pagination(page=1, page_size=1000, total=total, total_pages=total_pages)
    paginated = PaginatedData(items=schemas, pagination=pagination)
    response = ResponseModel(data=paginated)
    json_str = response.model_dump_json()
    print(f"  JSON serialization OK, length={len(json_str)}")
    
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n=== Testing Receipts serialization (closed AR endpoint uses get_receipts) ===")
try:
    items, total = finance_service.get_receipts(db, skip=0, limit=1000)
    print(f"  Service OK: {len(items)} items, total={total}")
    
    schemas = [Receipt.model_validate(item) for item in items]
    print(f"  Schema validation OK: {len(schemas)} items")
    for s in schemas:
        print(f"    {s.receipt_id} | invoice={s.invoice_id} | payer={s.payer} | receipt_date={s.receipt_date}")
    
except Exception as e:
    import traceback
    traceback.print_exc()

db.close()
