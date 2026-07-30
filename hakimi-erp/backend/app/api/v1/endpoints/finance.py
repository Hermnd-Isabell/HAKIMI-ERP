from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.finance import Invoice, InvoiceCreate, OpenAccountReceivable, ClosedAccountReceivable, Receipt, ReceiptCreate
from app.schemas.base import ResponseModel, PaginatedData, Pagination
from app.services.finance_service import finance_service

router = APIRouter()

# --- Invoice ---
@router.get("/invoices", response_model=ResponseModel[PaginatedData[Invoice]])
def read_invoices(db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = finance_service.get_invoices(db, skip=skip, limit=page_size)
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=len(items), total_pages=1)
    ))

@router.post("/invoices/from-delivery/{delivery_id}", response_model=ResponseModel[Invoice])
def create_from_delivery(delivery_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=finance_service.create_invoice_from_delivery(db, delivery_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/invoices/{invoice_id}", response_model=ResponseModel[Invoice])
def read_invoice(invoice_id: str, db: Session = Depends(get_db)):
    invoice = finance_service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return ResponseModel(data=invoice)

# --- Account Receivables ---
@router.get("/ar/open", response_model=ResponseModel[PaginatedData[OpenAccountReceivable]])
def read_open_ar(db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = finance_service.get_open_ar(db, skip=skip, limit=page_size)
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=len(items), total_pages=1)
    ))

@router.get("/ar/closed", response_model=ResponseModel[PaginatedData[ClosedAccountReceivable]])
def read_closed_ar(db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = finance_service.get_closed_ar(db, skip=skip, limit=page_size)
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=len(items), total_pages=1)
    ))

# --- Receipt & Clearing ---
@router.post("/receipts", response_model=ResponseModel[Receipt])
def post_receipt(receipt_in: ReceiptCreate, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=finance_service.post_receipt(db, receipt_in))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
