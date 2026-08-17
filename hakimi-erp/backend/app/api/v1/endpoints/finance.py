import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.core.database import get_db
from app.schemas.finance import (
    Invoice, InvoiceCreate,
    OpenAccountReceivable, ClosedAccountReceivable,
    Receipt, ReceiptCreate,
)
from app.schemas.base import ResponseModel, PaginatedData, Pagination
from app.services.finance_service import finance_service

router = APIRouter()


def _build_pagination(page: int, page_size: int, total: int) -> Pagination:
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages)


# --- Invoice ---
@router.get("/invoices", response_model=ResponseModel[PaginatedData[Invoice]])
def read_invoices(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20,
    customer: Optional[str] = None,
    invoice_no: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
):
    skip = (page - 1) * page_size
    items, total = finance_service.get_invoices(
        db, skip=skip, limit=page_size,
        customer=customer, invoice_no=invoice_no, status=status,
        date_from=date_from, date_to=date_to,
    )
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=_build_pagination(page, page_size, total),
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


@router.post("/invoices/{invoice_id}/void", response_model=ResponseModel[Invoice])
def void_invoice(invoice_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=finance_service.void_invoice(db, invoice_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoices/{invoice_id}/document-flow", response_model=ResponseModel[dict])
def read_document_flow(invoice_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=finance_service.get_document_flow(db, invoice_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Account Receivables ---
@router.get("/ar/open", response_model=ResponseModel[PaginatedData[OpenAccountReceivable]])
def read_open_ar(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20,
    customer: Optional[str] = None,
    invoice_no: Optional[str] = None,
    status: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = finance_service.get_open_ar(
        db, skip=skip, limit=page_size,
        customer=customer, invoice_no=invoice_no, status=status,
    )
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=_build_pagination(page, page_size, total),
    ))


@router.get("/ar/open/{invoice_id}", response_model=ResponseModel[OpenAccountReceivable])
def read_open_ar_by_invoice(invoice_id: str, db: Session = Depends(get_db)):
    ar = finance_service.get_open_ar_by_invoice(db, invoice_id)
    if not ar:
        raise HTTPException(status_code=404, detail="Open AR not found for this invoice")
    return ResponseModel(data=ar)


@router.get("/ar/closed", response_model=ResponseModel[PaginatedData[ClosedAccountReceivable]])
def read_closed_ar(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20,
    customer: Optional[str] = None,
    invoice_no: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = finance_service.get_closed_ar(
        db, skip=skip, limit=page_size,
        customer=customer, invoice_no=invoice_no,
    )
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=_build_pagination(page, page_size, total),
    ))


@router.get("/ar/closed/{invoice_id}", response_model=ResponseModel[list[ClosedAccountReceivable]])
def read_closed_ar_by_invoice(invoice_id: str, db: Session = Depends(get_db)):
    items = finance_service.get_closed_ar_by_invoice(db, invoice_id)
    return ResponseModel(data=items)


# --- Receipt & Clearing ---
@router.get("/receipts", response_model=ResponseModel[PaginatedData[Receipt]])
def read_receipts(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20,
    customer: Optional[str] = None,
    invoice_no: Optional[str] = None,
):
    skip = (page - 1) * page_size
    items, total = finance_service.get_receipts(
        db, skip=skip, limit=page_size,
        invoice_no=invoice_no, payer=customer,
    )
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=_build_pagination(page, page_size, total),
    ))


@router.get("/receipts/{receipt_id}", response_model=ResponseModel[Receipt])
def read_receipt(receipt_id: str, db: Session = Depends(get_db)):
    receipt = finance_service.get_receipt(db, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return ResponseModel(data=receipt)


@router.post("/receipts", response_model=ResponseModel[Receipt])
def post_receipt(receipt_in: ReceiptCreate, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=finance_service.post_receipt(db, receipt_in))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
