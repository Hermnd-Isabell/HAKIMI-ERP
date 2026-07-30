from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.material import Material, MaterialCreate, MaterialUpdate
from app.schemas.base import ResponseModel, PaginatedData, Pagination
from app.services.material_service import material_service

router = APIRouter()

@router.get("/", response_model=ResponseModel[PaginatedData[Material]])
def read_materials(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 20
):
    skip = (page - 1) * page_size
    materials = material_service.get_materials(db, skip=skip, limit=page_size)
    total = len(materials) 
    
    return ResponseModel(
        data=PaginatedData(
            items=materials,
            pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=1)
        )
    )

@router.post("/", response_model=ResponseModel[Material], status_code=status.HTTP_201_CREATED)
def create_material(
    *,
    db: Session = Depends(get_db),
    material_in: MaterialCreate
):
    db_material = material_service.get_material(db, material_id=material_in.material_id)
    if db_material:
        raise HTTPException(
            status_code=400,
            detail="Material with this ID already exists.",
        )
    material = material_service.create_material(db, material_in=material_in)
    return ResponseModel(data=material)

@router.get("/{material_id}", response_model=ResponseModel[Material])
def read_material(
    material_id: str,
    db: Session = Depends(get_db)
):
    material = material_service.get_material(db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return ResponseModel(data=material)

@router.patch("/{material_id}", response_model=ResponseModel[Material])
def update_material(
    material_id: str,
    material_in: MaterialUpdate,
    db: Session = Depends(get_db)
):
    material = material_service.update_material(db, material_id=material_id, material_in=material_in)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return ResponseModel(data=material)

@router.delete("/{material_id}", response_model=ResponseModel[bool])
def delete_material(
    material_id: str,
    db: Session = Depends(get_db)
):
    success = material_service.delete_material(db, material_id=material_id)
    if not success:
        raise HTTPException(status_code=404, detail="Material not found")
    return ResponseModel(data=True)
