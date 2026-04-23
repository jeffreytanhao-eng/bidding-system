
import uuid
from sqlalchemy import Column, String, Text, DateTime, UUID, DECIMAL, ForeignKey, CheckConstraint, BigInteger, Boolean
from sqlalchemy.sql import func
from src.utils.database import Base


class Tender(Base):
    __tablename__ = "tenders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_no = Column(String(100), unique=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    requirements = Column(Text)
    budget = Column(DECIMAL(15, 2))
    deadline = Column(DateTime(timezone=True))
    open_time = Column(DateTime(timezone=True))
    procurement_method = Column(String(50), default='public_bidding')
    status = Column(String(20), default='draft')
    business_weight = Column(DECIMAL(3, 2), default=0.4)
    technical_weight = Column(DECIMAL(3, 2), default=0.6)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("status IN ('draft', 'published', 'reviewing', 'completed', 'cancelled')", name='check_tender_status'),
    )


class TenderAttachment(Base):
    __tablename__ = "tender_attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey('tenders.id', ondelete='CASCADE'), nullable=False)
    filename = Column(String(200), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger)
    file_type = Column(String(50))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())


class TenderInvitee(Base):
    __tablename__ = "tender_invitees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey('tenders.id', ondelete='CASCADE'), nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'), nullable=False)
    invite_token = Column(String(100), unique=True, nullable=False)
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

