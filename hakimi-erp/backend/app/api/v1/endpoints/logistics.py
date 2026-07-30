from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.logistics import Delivery, DeliveryCreate
from app.schemas.base import ResponseModel, PaginatedData, Pagination
from app.services.logistics_service import logistics_service

router = APIRouter()

# --- Delivery ---
@router.get("/deliveries", response_model=ResponseModel[PaginatedData[Delivery]])
def read_deliveries(db: Session = Depends(get_db), page: int = 1, page_size: int = 20):
    skip = (page - 1) * page_size
    items = logistics_service.get_deliveries(db, skip=skip, limit=page_size)
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=len(items), total_pages=1)
    ))

@router.post("/deliveries", response_model=ResponseModel[Delivery], status_code=status.HTTP_201_CREATED)
def create_delivery(delivery_in: DeliveryCreate, db: Session = Depends(get_db)):
    return ResponseModel(data=logistics_service.create_delivery(db, delivery_in))

@router.get("/deliveries/{delivery_id}", response_model=ResponseModel[Delivery])
def read_delivery(delivery_id: str, db: Session = Depends(get_db)):
    delivery = logistics_service.get_delivery(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return ResponseModel(data=delivery)

@router.post("/deliveries/from-so/{sales_order_id}", response_model=ResponseModel[Delivery])
def create_from_so(sales_order_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=logistics_service.create_from_sales_order(db, sales_order_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- PGI ---
@router.post("/deliveries/{delivery_id}/pgi", response_model=ResponseModel[Delivery])
def post_goods_issue(delivery_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=logistics_service.post_goods_issue(db, delivery_id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
