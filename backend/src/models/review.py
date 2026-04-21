
import uuid
from sqlalchemy import Column, String, Text, DateTime, UUID, Integer, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from src.utils.database import Base


class Reviewer(Base):
    __tablename__ = "reviewers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey('tenders.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    dingtalk_user_id = Column(String(100))
    review_type = Column(String(20), nullable=False)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("review_type IN ('business', 'technical')", name='check_review_type'),
        CheckConstraint("status IN ('pending', 'notified', 'in_progress', 'completed')", name='check_reviewer_status'),
    )


class ReviewScore(Base):
    __tablename__ = "review_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey('reviewers.id', ondelete='CASCADE'), nullable=False)
    bid_id = Column(UUID(as_uuid=True), ForeignKey('bids.id'), nullable=False)
    price_score = Column(Integer)
    qualification_score = Column(Integer)
    experience_score = Column(Integer)
    service_score = Column(Integer)
    total_score = Column(DECIMAL(5, 2))
    comment = Column(Text)
    recommendation = Column(String(20))
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("price_score BETWEEN 0 AND 100", name='check_price_score'),
        CheckConstraint("qualification_score BETWEEN 0 AND 100", name='check_qualification_score'),
        CheckConstraint("experience_score BETWEEN 0 AND 100", name='check_experience_score'),
        CheckConstraint("service_score BETWEEN 0 AND 100", name='check_service_score'),
        CheckConstraint("recommendation IN ('recommend', 'neutral', 'not_recommend')", name='check_recommendation'),
    )

