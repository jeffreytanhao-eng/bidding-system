
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ApiResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    total: int
    items: list
    page: int
    page_size: int

