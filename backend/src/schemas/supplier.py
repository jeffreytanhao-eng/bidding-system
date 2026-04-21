
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    business_scope: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    business_scope: Optional[str] = None
    rating: Optional[str] = None
    status: Optional[str] = None


class Supplier(SupplierBase):
    id: UUID
    rating: str = "C"
    status: str = "active"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SupplierTagBase(BaseModel):
    name: str
    description: Optional[str] = None


class SupplierTagCreate(SupplierTagBase):
    pass


class SupplierTag(SupplierTagBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

