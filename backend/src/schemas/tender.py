
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class TenderBase(BaseModel):
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    budget: Optional[Decimal] = None
    deadline: datetime
    business_weight: Decimal = Decimal("0.4")
    technical_weight: Decimal = Decimal("0.6")


class TenderCreate(TenderBase):
    pass


class TenderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    budget: Optional[Decimal] = None
    deadline: Optional[datetime] = None
    business_weight: Optional[Decimal] = None
    technical_weight: Optional[Decimal] = None
    status: Optional[str] = None


class Tender(TenderBase):
    id: UUID
    status: str = "draft"
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TenderAttachmentBase(BaseModel):
    filename: str
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None


class TenderAttachmentCreate(TenderAttachmentBase):
    tender_id: UUID


class TenderAttachment(TenderAttachmentBase):
    id: UUID
    tender_id: UUID
    uploaded_at: datetime

    class Config:
        from_attributes = True


class TenderInviteeBase(BaseModel):
    tender_id: UUID
    supplier_id: UUID
    invite_token: str


class TenderInviteeCreate(TenderInviteeBase):
    pass


class TenderInvitee(TenderInviteeBase):
    id: UUID
    email_sent: bool = False
    email_sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

