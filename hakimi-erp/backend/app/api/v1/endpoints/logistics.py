from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.logistics import (
    Delivery, DeliveryCreate, DeliveryListItem,
    GoodsIssue, get_status_label, get_status_index,
    PartialPgiRequest, PickBatchRequest, PickRecord
)
from app.schemas.base import ResponseModel, PaginatedData, Pagination
from app.services.logistics_service import logistics_service
from app.models.logistics import StorageLocation

router = APIRouter()

# --- Delivery Listing (with filters) ---
@router.get("/deliveries", response_model=ResponseModel[PaginatedData[DeliveryListItem]])
def read_deliveries(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=1000),
    delivery_no: Optional[str] = Query(None),
    sales_order_no: Optional[str] = Query(None),
    customer_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    skip = (page - 1) * page_size
    items, total = logistics_service.get_deliveries(
        db, skip=skip, limit=page_size,
        delivery_no=delivery_no,
        sales_order_no=sales_order_no,
        customer_name=customer_name,
        status=status,
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return ResponseModel(data=PaginatedData(
        items=items,
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages)
    ))

@router.post("/deliveries", response_model=ResponseModel[Delivery], status_code=status.HTTP_201_CREATED)
def create_delivery(delivery_in: DeliveryCreate, db: Session = Depends(get_db)):
    return ResponseModel(data=logistics_service.create_delivery(db, delivery_in))

# --- Delivery Detail ---
@router.get("/deliveries/{delivery_id}", response_model=ResponseModel[Delivery])
def read_delivery(delivery_id: str, db: Session = Depends(get_db)):
    delivery = logistics_service.get_delivery_detail(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return ResponseModel(data=delivery)

# --- Create Delivery from Sales Order ---
@router.post("/deliveries/from-so/{sales_order_id}", response_model=ResponseModel[Delivery])
def create_from_so(sales_order_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=logistics_service.create_from_sales_order(db, sales_order_id))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# --- Batch Picking ---
@router.post("/deliveries/{delivery_id}/start-picking", response_model=ResponseModel[Delivery])
def start_picking(delivery_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=logistics_service.start_picking(db, delivery_id))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/deliveries/{delivery_id}/pick-batch", response_model=ResponseModel[Delivery])
def pick_batch(delivery_id: str, body: PickBatchRequest, db: Session = Depends(get_db)):
    try:
        items_dict = {it.delivery_item_id: it.quantity for it in body.items}
        return ResponseModel(data=logistics_service.pick_batch(
            db, delivery_id, items_dict,
            storage_location=body.storage_location,
            picked_by=body.picked_by,
        ))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/deliveries/{delivery_id}/confirm-picking", response_model=ResponseModel[Delivery])
def confirm_picking(delivery_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=logistics_service.confirm_picking(db, delivery_id))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/deliveries/{delivery_id}/pick-records", response_model=ResponseModel[List[PickRecord]])
def read_pick_records(delivery_id: str, db: Session = Depends(get_db)):
    delivery = logistics_service.get_delivery(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    pr_list = logistics_service.get_pick_records(db, delivery_id)
    return ResponseModel(data=pr_list)

# --- Ship ---
@router.post("/deliveries/{delivery_id}/ship", response_model=ResponseModel[Delivery])
def ship_delivery(delivery_id: str, db: Session = Depends(get_db)):
    try:
        return ResponseModel(data=logistics_service.ship_delivery(db, delivery_id))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# --- Post Goods Issue (PGI) ---
@router.post("/deliveries/{delivery_id}/pgi", response_model=ResponseModel[Delivery])
def post_goods_issue(delivery_id: str, body: PartialPgiRequest = None, db: Session = Depends(get_db)):
    try:
        partial_map = None
        if body and body.items:
            partial_map = {it.delivery_item_id: it.quantity for it in body.items}
        return ResponseModel(data=logistics_service.post_goods_issue(db, delivery_id, partial_map))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# --- Goods Issue Records ---
@router.get("/deliveries/{delivery_id}/goods-issues", response_model=ResponseModel[List[GoodsIssue]])
def read_goods_issues(delivery_id: str, db: Session = Depends(get_db)):
    delivery = logistics_service.get_delivery(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    gi_list = logistics_service.get_goods_issues(db, delivery_id)
    return ResponseModel(data=gi_list)

# --- SO Item Remaining Quantities ---
@router.get("/sales-orders/{sales_order_id}/remaining-quantities")
def get_so_remaining(sales_order_id: str, db: Session = Depends(get_db)):
    result = logistics_service.get_so_remaining_quantities(db, sales_order_id)
    return ResponseModel(data=result)

# --- Storage Locations (F4 Search) ---
@router.get("/storage-locations")
def search_storage_locations(
    keyword: str = Query(""),
    plant: str = Query(""),
    db: Session = Depends(get_db),
):
    query = db.query(StorageLocation)
    if keyword:
        query = query.filter(
            (StorageLocation.sloc_id.like(f"%{keyword}%")) |
            (StorageLocation.sloc_name.like(f"%{keyword}%")) |
            (StorageLocation.storage_bin.like(f"%{keyword}%"))
        )
    if plant:
        query = query.filter(StorageLocation.plant == plant)
    results = query.order_by(StorageLocation.sloc_id).limit(50).all()
    return ResponseModel(data=[
        {
            "sloc_id": r.sloc_id,
            "sloc_name": r.sloc_name,
            "plant": r.plant,
            "warehouse_no": r.warehouse_no,
            "storage_type": r.storage_type,
            "storage_bin": r.storage_bin,
            "description": r.description,
        }
        for r in results
    ])

# --- Status Mapping Utility ---
@router.get("/delivery-status-labels")
def get_status_labels():
    from app.schemas.logistics import DELIVERY_STATUS_LABELS
    return ResponseModel(data=DELIVERY_STATUS_LABELS)