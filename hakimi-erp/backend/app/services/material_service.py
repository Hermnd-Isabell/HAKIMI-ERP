from sqlalchemy.orm import Session
from app.models.material import Material
from app.schemas.material import MaterialCreate, MaterialUpdate
from typing import List, Optional

class MaterialService:
    @staticmethod
    def get_materials(db: Session, skip: int = 0, limit: int = 100) -> List[Material]:
        return db.query(Material).offset(skip).limit(limit).all()

    @staticmethod
    def get_material(db: Session, material_id: str) -> Optional[Material]:
        return db.query(Material).filter(Material.material_id == material_id).first()

    @staticmethod
    def create_material(db: Session, material_in: MaterialCreate) -> Material:
        db_material = Material(**material_in.model_dump())
        db.add(db_material)
        db.commit()
        db.refresh(db_material)
        return db_material

    @staticmethod
    def update_material(db: Session, material_id: str, material_in: MaterialUpdate) -> Optional[Material]:
        db_material = MaterialService.get_material(db, material_id)
        if not db_material:
            return None
        
        update_data = material_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_material, field, value)
        
        db.commit()
        db.refresh(db_material)
        return db_material

    @staticmethod
    def delete_material(db: Session, material_id: str) -> bool:
        db_material = MaterialService.get_material(db, material_id)
        if not db_material:
            return False
        
        db.delete(db_material)
        db.commit()
        return True

material_service = MaterialService()
