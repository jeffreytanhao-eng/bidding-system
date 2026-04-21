
import uuid
from sqlalchemy import Column, String, DateTime, UUID, CheckConstraint
from sqlalchemy.sql import func
from src.utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    dingtalk_user_id = Column(String(100), unique=True)
    role = Column(String(20), default='reviewer')
    status = Column(String(20), default='active')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'tender_manager', 'reviewer')", name='check_user_role'),
        CheckConstraint("status IN ('active', 'inactive')", name='check_user_status'),
    )

