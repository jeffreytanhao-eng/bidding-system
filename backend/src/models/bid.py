
import uuid
from sqlalchemy import Column, String, Text, DateTime, UUID, DECIMAL, ForeignKey, CheckConstraint, BigInteger
from sqlalchemy.sql import func
from src.utils.database import Base


class Bid(Base):
    __tablename__ = "bids"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey('tenders.id', ondelete='CASCADE'), nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'), nullable=False)
    quote_amount = Column(DECIMAL(15, 2))
    delivery_period = Column(String(100))
    contact_person = Column(String(50))
    contact_phone = Column(String(20))
    technical_summary = Column(Text)
    status = Column(String(20), default='submitted')
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('submitted', 'reviewing', 'passed', 'rejected')", name='check_bid_status'),
    )


class BidFile(Base):
    __tablename__ = "bid_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = Column(UUID(as_uuid=True), ForeignKey('bids.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(20), nullable=False)
    filename = Column(String(200), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger)
    file_type = Column(String(50))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("type IN ('business', 'technical')", name='check_bid_file_type'),
    )

