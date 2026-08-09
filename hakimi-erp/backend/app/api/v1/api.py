from fastapi import APIRouter
from app.api.v1.endpoints import customer, material, sales, logistics, finance, report

api_router = APIRouter()
api_router.include_router(customer.router, prefix="/master/partners", tags=["Customer Master"])
api_router.include_router(material.router, prefix="/master/materials", tags=["Material Master"])
api_router.include_router(sales.router, prefix="/sales", tags=["Sales Management"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])
api_router.include_router(finance.router, prefix="/finance", tags=["Finance"])
api_router.include_router(report.router, prefix="/reports", tags=["Reports"])