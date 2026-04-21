
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.bid_service import BidService
from src.schemas.bid import Bid, BidCreate
from src.schemas.common import ApiResponse

router = APIRouter(prefix="/bids", tags=["应标管理"])


@router.get("/submit/{token}", response_model=ApiResponse)
def get_bid_form(token: str, db: Session = Depends(get_db)):
    invitee = BidService.validate_invite_token(db, token)
    if not invitee:
        raise HTTPException(status_code=400, detail="无效的应标令牌")
    return ApiResponse(data={"invite_token": token, "valid": True})


@router.post("", response_model=ApiResponse)
def submit_bid(data: BidCreate, db: Session = Depends(get_db)):
    try:
        bid = BidService.submit_bid(db, data.invite_token, data)
        return ApiResponse(data=Bid.model_validate(bid))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tender/{tender_id}", response_model=ApiResponse)
def list_bids(tender_id: UUID, db: Session = Depends(get_db)):
    bids = BidService.get_bids_by_tender(db, tender_id)
    return ApiResponse(data=[Bid.model_validate(b) for b in bids])


@router.get("/{id}", response_model=ApiResponse)
def get_bid_detail(id: UUID, db: Session = Depends(get_db)):
    bid = BidService.get_bid(db, id)
    if not bid:
        raise HTTPException(status_code=404, detail="应标不存在")
    return ApiResponse(data=Bid.model_validate(bid))

