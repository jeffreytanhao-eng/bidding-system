
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class BidBase(BaseModel):
    quote_amount: Optional[Decimal] = None
    delivery_period: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    technical_summary: Optional[str] = None


class BidCreate(BidBase):
    invite_token: str


class BidUpdate(BaseModel):
    quote_amount: Optional[Decimal] = None
    delivery_period: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    technical_summary: Optional[str] = None
    status: Optional[str] = None


class Bid(BidBase):
    id: UUID
    tender_id: UUID
    supplier_id: UUID
    status: str = "submitted"
    submitted_at: datetime

    class Config:
        from_attributes = True


class BidFileBase(BaseModel):
    type: str
    filename: str
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None


class BidFileCreate(BidFileBase):
    bid_id: UUID


class BidFile(BidFileBase):
    id: UUID
    bid_id: UUID
    uploaded_at: datetime

    class Config:
        from_attributes = True

