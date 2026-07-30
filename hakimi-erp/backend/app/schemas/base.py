from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime

DataT = TypeVar("DataT")

class Pagination(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    total: int = 0
    total_pages: int = 0

class ResponseModel(BaseModel, Generic[DataT]):
    success: bool = True
    trace_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    code: str = "OK"
    message: str = "操作成功"
    data: Optional[DataT] = None
    errors: Optional[List[Any]] = None

class PaginatedData(BaseModel, Generic[DataT]):
    items: List[DataT]
    pagination: Pagination
