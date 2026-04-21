
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.review_service import ReviewService
from src.schemas.review import Reviewer, ScoreCreate, ReviewScore
from src.schemas.common import ApiResponse

router = APIRouter(tags=["评审管理"])


@router.post("/dingtalk/sync", response_model=ApiResponse)
async def sync_dingtalk(db: Session = Depends(get_db)):
    return ApiResponse(message="钉钉同步功能")


@router.get("/dingtalk/departments", response_model=ApiResponse)
def get_departments(db: Session = Depends(get_db)):
    return ApiResponse(data=[])


@router.get("/dingtalk/users", response_model=ApiResponse)
def get_users(db: Session = Depends(get_db)):
    return ApiResponse(data=[])


@router.post("/tender/{id}/reviewers", response_model=ApiResponse)
def assign_reviewers(id: UUID, reviewers: List[dict], db: Session = Depends(get_db)):
    try:
        result = ReviewService.assign_reviewers(db, id, reviewers)
        return ApiResponse(data=[Reviewer.model_validate(r) for r in result])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tender/{id}/start-review", response_model=ApiResponse)
async def start_review(id: UUID, db: Session = Depends(get_db)):
    try:
        result = await ReviewService.start_review(db, id)
        return ApiResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my", response_model=ApiResponse)
def get_my_reviews(db: Session = Depends(get_db)):
    return ApiResponse(data=[])


@router.post("/{id}/score", response_model=ApiResponse)
def submit_score(id: UUID, bid_id: UUID, score_data: ScoreCreate, db: Session = Depends(get_db)):
    try:
        score = ReviewService.submit_score(db, id, bid_id, score_data)
        return ApiResponse(data=ReviewScore.model_validate(score))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tender/{id}/progress", response_model=ApiResponse)
def get_progress(id: UUID, db: Session = Depends(get_db)):
    try:
        progress = ReviewService.get_review_progress(db, id)
        return ApiResponse(data=progress)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tender/{id}/remind", response_model=ApiResponse)
async def remind_reviewers(id: UUID, db: Session = Depends(get_db)):
    try:
        count = await ReviewService.remind_reviewers(db, id)
        return ApiResponse(data={"reminded_count": count})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
