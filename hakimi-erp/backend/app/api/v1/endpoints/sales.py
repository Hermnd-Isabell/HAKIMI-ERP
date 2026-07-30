from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.sales import (
    Inquiry, InquiryCreate,
    Quotation, QuotationCreate,
    SalesOrder, SalesOrderCreate
)
from app.schemas.base import ResponseModel, PaginatedData, Pagination
from app.services.sales_service import sales_service

router = APIRouter()

# --- Inquiry ---
@router.get("/inquiries", response_model=ResponseModel[PaginatedData[Inquiry]])
def read_inquiries(db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = sales_service.get_inquiries(db, skip=skip, limit=page_size)
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=len(items), total_pages=1)
    ))

@router.post("/inquiries", response_model=ResponseModel[Inquiry], status_code=status.HTTP_201_CREATED)
def create_inquiry(inquiry_in: InquiryCreate, db: Session = Depends(get_db)):
    return ResponseModel(data=sales_service.create_inquiry(db, inquiry_in))

@router.get("/inquiries/{inquiry_id}", response_model=ResponseModel[Inquiry])
def read_inquiry(inquiry_id: str, db: Session = Depends(get_db)):
    inquiry = sales_service.get_inquiry(db, inquiry_id)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return ResponseModel(data=inquiry)

# --- Quotation ---
@router.get("/quotations", response_model=ResponseModel[PaginatedData[Quotation]])
def read_quotations(db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = sales_service.get_quotations(db, skip=skip, limit=page_size)
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=len(items), total_pages=1)
    ))

@router.post("/quotations", response_model=ResponseModel[Quotation], status_code=status.HTTP_201_CREATED)
def create_quotation(quotation_in: QuotationCreate, db: Session = Depends(get_db)):
    return ResponseModel(data=sales_service.create_quotation(db, quotation_in))

@router.get("/quotations/{quotation_id}", response_model=ResponseModel[Quotation])
def read_quotation(quotation_id: str, db: Session = Depends(get_db)):
    quotation = sales_service.get_quotation(db, quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return ResponseModel(data=quotation)

# --- Sales Order ---
@router.get("/orders", response_model=ResponseModel[PaginatedData[SalesOrder]])
def read_orders(db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = sales_service.get_orders(db, skip=skip, limit=page_size)
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=len(items), total_pages=1)
    ))

@router.post("/orders", response_model=ResponseModel[SalesOrder], status_code=status.HTTP_201_CREATED)
def create_order(order_in: SalesOrderCreate, db: Session = Depends(get_db)):
    return ResponseModel(data=sales_service.create_order(db, order_in))

@router.get("/orders/{order_id}", response_model=ResponseModel[SalesOrder])
def read_order(order_id: str, db: Session = Depends(get_db)):
    order = sales_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return ResponseModel(data=order)
