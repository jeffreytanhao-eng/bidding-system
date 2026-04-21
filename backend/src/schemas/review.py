
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal


class ReviewerBase(BaseModel):
    tender_id: UUID
    user_id: UUID
    dingtalk_user_id: Optional[str] = None
    review_type: str


class ReviewerCreate(ReviewerBase):
    pass


class ReviewerUpdate(BaseModel):
    status: Optional[str] = None


class Reviewer(ReviewerBase):
    id: UUID
    status: str = "pending"
    created_at: datetime

    class Config:
        from_attributes = True


class ScoreCreate(BaseModel):
    price_score: Optional[int] = None
    qualification_score: Optional[int] = None
    experience_score: Optional[int] = None
    service_score: Optional[int] = None
    comment: Optional[str] = None
    recommendation: Optional[str] = None

    @field_validator('price_score', 'qualification_score', 'experience_score', 'service_score')
    @classmethod
    def validate_score_range(cls, v):
        if v is not None and (v &lt; 0 or v &gt; 100):
            raise ValueError('评分必须在0-100之间')
        return v


class ReviewScoreBase(BaseModel):
    price_score: Optional[int] = None
    qualification_score: Optional[int] = None
    experience_score: Optional[int] = None
    service_score: Optional[int] = None
    total_score: Optional[Decimal] = None
    comment: Optional[str] = None
    recommendation: Optional[str] = None


class ReviewScoreCreate(ReviewScoreBase):
    reviewer_id: UUID
    bid_id: UUID


class ReviewScore(ReviewScoreBase):
    id: UUID
    reviewer_id: UUID
    bid_id: UUID
    submitted_at: datetime

    class Config:
        from_attributes = True

