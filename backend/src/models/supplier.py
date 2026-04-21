
import uuid
from sqlalchemy import Column, String, Text, DateTime, UUID, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.utils.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(50))
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    address = Column(String(500))
    business_scope = Column(Text)
    rating = Column(String(1), default='C')
    status = Column(String(20), default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("rating IN ('A', 'B', 'C', 'D')", name='check_supplier_rating'),
        CheckConstraint("status IN ('active', 'inactive', 'blacklist')", name='check_supplier_status'),
    )


class SupplierTag(Base):
    __tablename__ = "supplier_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

