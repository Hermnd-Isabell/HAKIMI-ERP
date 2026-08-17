from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.report_service import report_service
from app.schemas.base import ResponseModel
from typing import Optional

router = APIRouter()

@router.get("/sales-performance", response_model=ResponseModel)
def sales_performance(days: int = 30, db: Session = Depends(get_db)):
    return ResponseModel(data=report_service.get_sales_performance(db, days))

@router.get("/financial-summary", response_model=ResponseModel)
def financial_summary(db: Session = Depends(get_db)):
    return ResponseModel(data=report_service.get_financial_summary(db))

@router.get("/financial-detail", response_model=ResponseModel)
def financial_detail(db: Session = Depends(get_db)):
    return ResponseModel(data=report_service.get_financial_detail(db))

@router.get("/delivery-stats", response_model=ResponseModel)
def delivery_stats(db: Session = Depends(get_db)):
    return ResponseModel(data=report_service.get_delivery_stats(db))

@router.get("/dashboard-summary", response_model=ResponseModel)
def dashboard_summary(db: Session = Depends(get_db)):
    return ResponseModel(data=report_service.get_dashboard_summary(db))

