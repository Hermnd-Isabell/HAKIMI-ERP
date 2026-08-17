from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.schemas.customer import BusinessPartner, BusinessPartnerCreate, BusinessPartnerUpdate
from app.schemas.base import ResponseModel, PaginatedData, Pagination
from app.services.customer_service import customer_service

router = APIRouter()

@router.get("/", response_model=ResponseModel[PaginatedData[BusinessPartner]])
def read_partners(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20
):
    skip = (page - 1) * page_size
    partners = customer_service.get_partners(db, skip=skip, limit=page_size)
    # Simple pagination mock for now
    total = len(partners) 
    
    return ResponseModel(
        data=PaginatedData(
            items=partners,
            pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=1)
        )
    )

@router.post("/", response_model=ResponseModel[BusinessPartner], status_code=status.HTTP_201_CREATED)
def create_partner(
    *,
    db: Session = Depends(get_db),
    partner_in: BusinessPartnerCreate
):
    db_partner = customer_service.get_partner(db, bp_id=partner_in.bp_id)
    if db_partner:
        raise HTTPException(
            status_code=400,
            detail="Business Partner with this ID already exists.",
        )
    partner = customer_service.create_partner(db, partner_in=partner_in)
    return ResponseModel(data=partner)

@router.get("/{bp_id}", response_model=ResponseModel[BusinessPartner])
def read_partner(
    bp_id: str,
    db: Session = Depends(get_db)
):
    partner = customer_service.get_partner(db, bp_id=bp_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return ResponseModel(data=partner)

@router.patch("/{bp_id}", response_model=ResponseModel[BusinessPartner])
def update_partner(
    bp_id: str,
    partner_in: BusinessPartnerUpdate,
    db: Session = Depends(get_db)
):
    partner = customer_service.update_partner(db, bp_id=bp_id, partner_in=partner_in)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return ResponseModel(data=partner)

@router.delete("/{bp_id}", response_model=ResponseModel[bool])
def delete_partner(
    bp_id: str,
    db: Session = Depends(get_db)
):
    success = customer_service.delete_partner(db, bp_id=bp_id)
    if not success:
        raise HTTPException(status_code=404, detail="Partner not found")
    return ResponseModel(data=True)
