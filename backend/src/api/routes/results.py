
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.result_service import ResultService
from src.schemas.common import ApiResponse

router = APIRouter(tags=["中标管理"])


@router.post("/tender/{id}/summary", response_model=ApiResponse)
def calculate_summary(id: UUID, db: Session = Depends(get_db)):
    try:
        summary = ResultService.calculate_summary(db, id)
        return ApiResponse(data={"tender_id": str(id), "summary": summary})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tender/{id}/weights", response_model=ApiResponse)
def set_weights(id: UUID, business_weight: float, technical_weight: float, db: Session = Depends(get_db)):
    try:
        tender = ResultService.set_weights(db, id, business_weight, technical_weight)
        return ApiResponse(data={"tender_id": str(id), "business_weight": float(tender.business_weight), "technical_weight": float(tender.technical_weight)})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tender/{id}/recommendation", response_model=ApiResponse)
def get_recommendation(id: UUID, db: Session = Depends(get_db)):
    try:
        summary = ResultService.calculate_summary(db, id)
        return ApiResponse(data=summary)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tender/{id}/approve", response_model=ApiResponse)
def approve_result(id: UUID, winner_bid_id: UUID, approver_id: UUID, db: Session = Depends(get_db)):
    try:
        result = ResultService.approve_result(db, id, winner_bid_id, approver_id)
        return ApiResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tender/{id}/announce", response_model=ApiResponse)
async def announce_result(id: UUID, db: Session = Depends(get_db)):
    try:
        result = await ResultService.announce_result(db, id)
        return ApiResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
