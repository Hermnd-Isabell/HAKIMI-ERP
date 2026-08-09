"""Quick test: can we even connect to DB and query?"""
import sys, traceback
sys.path.insert(0, r"E:\Tongji University\2026SDsystem\HAKIMI-ERP\hakimi-erp\backend")

try:
    from app.core.database import SessionLocal, engine
    from sqlalchemy import text
    db = SessionLocal()
    print("DB session created OK")
    
    result = db.execute(text("SELECT 1"))
    print("SELECT 1 =>", result.fetchone())
    
    result2 = db.execute(text("SELECT COUNT(*) FROM invoice"))
    print("invoice count =>", result2.fetchone())
    
    result3 = db.execute(text("SELECT COUNT(*) FROM business_partner"))
    print("partner count =>", result3.fetchone())
    
    db.close()
    print("\nAll DB queries OK")
except Exception as e:
    traceback.print_exc()
