from sqlalchemy.orm import Session
from app.models.sales import Inquiry, InquiryItem, Quotation, QuotationItem, SalesOrder, SalesOrderItem
from app.schemas.sales import (
    InquiryCreate, QuotationCreate, SalesOrderCreate,
    InquiryItemCreate, QuotationItemCreate, SalesOrderItemCreate
)
from typing import List, Optional
from datetime import datetime

class SalesService:
    # --- Inquiry ---
    @staticmethod
    def get_inquiries(db: Session, skip: int = 0, limit: int = 100) -> List[Inquiry]:
        return db.query(Inquiry).offset(skip).limit(limit).all()

    @staticmethod
    def get_inquiry(db: Session, inquiry_id: str) -> Optional[Inquiry]:
        return db.query(Inquiry).filter(Inquiry.inquiry_id == inquiry_id).first()

    @staticmethod
    def create_inquiry(db: Session, inquiry_in: InquiryCreate) -> Inquiry:
        data = inquiry_in.model_dump()
        items_data = data.pop("items")
        db_inquiry = Inquiry(**data)
        db.add(db_inquiry)
        
        for item in items_data:
            db_item = InquiryItem(**item, inquiry_id=db_inquiry.inquiry_id)
            db.add(db_item)
            
        db.commit()
        db.refresh(db_inquiry)
        return db_inquiry

    # --- Quotation ---
    @staticmethod
    def get_quotations(db: Session, skip: int = 0, limit: int = 100) -> List[Quotation]:
        return db.query(Quotation).offset(skip).limit(limit).all()

    @staticmethod
    def get_quotation(db: Session, quotation_id: str) -> Optional[Quotation]:
        return db.query(Quotation).filter(Quotation.quotation_id == quotation_id).first()

    @staticmethod
    def create_quotation(db: Session, quotation_in: QuotationCreate) -> Quotation:
        data = quotation_in.model_dump()
        items_data = data.pop("items")
        db_quotation = Quotation(**data)
        db.add(db_quotation)
        
        for item in items_data:
            db_item = QuotationItem(**item, quotation_id=db_quotation.quotation_id)
            db.add(db_item)
        
        # If created from inquiry, close the inquiry
        if db_quotation.inquiry_id:
            db_inquiry = SalesService.get_inquiry(db, db_quotation.inquiry_id)
            if db_inquiry:
                db_inquiry.status = "CLOSED"
            
        db.commit()
        db.refresh(db_quotation)
        return db_quotation

    # --- Sales Order ---
    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[SalesOrder]:
        return db.query(SalesOrder).offset(skip).limit(limit).all()

    @staticmethod
    def get_order(db: Session, sales_order_id: str) -> Optional[SalesOrder]:
        return db.query(SalesOrder).filter(SalesOrder.sales_order_id == sales_order_id).first()

    @staticmethod
    def create_order(db: Session, order_in: SalesOrderCreate) -> SalesOrder:
        data = order_in.model_dump()
        items_data = data.pop("items")
        db_order = SalesOrder(**data)
        db.add(db_order)
        
        for item in items_data:
            db_item = SalesOrderItem(**item, sales_order_id=db_order.sales_order_id)
            # Simulate ATP: confirm quantity
            db_item.confirmed_quantity = db_item.order_quantity
            db_item.availability_status = "CONFIRMED"
            db.add(db_item)
            
        # If created from quotation, close the quotation
        if db_order.quotation_id:
            db_quotation = SalesService.get_quotation(db, db_order.quotation_id)
            if db_quotation:
                db_quotation.status = "CLOSED"
                
        db.commit()
        db.refresh(db_order)
        return db_order

sales_service = SalesService()
