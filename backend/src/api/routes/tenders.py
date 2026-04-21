
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.tender_service import TenderService
from src.schemas.tender import Tender, TenderCreate, TenderUpdate, TenderInvitee
from src.schemas.common import ApiResponse

router = APIRouter(prefix="/tenders", tags=["标书管理"])


@router.post("", response_model=ApiResponse)
def create_tender(data: TenderCreate, db: Session = Depends(get_db)):
    try:
        tender = TenderService.create_tender(db, data)
        return ApiResponse(data=Tender.model_validate(tender))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=ApiResponse)
def update_tender(id: UUID, data: TenderUpdate, db: Session = Depends(get_db)):
    try:
        tender = TenderService.update_tender(db, id, data)
        return ApiResponse(data=Tender.model_validate(tender))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=ApiResponse)
def list_tenders(status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    tenders = TenderService.get_tenders(db, status)
    return ApiResponse(data=[Tender.model_validate(t) for t in tenders])


@router.get("/{id}", response_model=ApiResponse)
def get_tender(id: UUID, db: Session = Depends(get_db)):
    tender = TenderService.get_tender(db, id)
    if not tender:
        raise HTTPException(status_code=404, detail="标书不存在")
    return ApiResponse(data=Tender.model_validate(tender))


@router.post("/{id}/attachments", response_model=ApiResponse)
def upload_attachment(id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        attachment = TenderService.upload_attachment(db, id, file)
        return ApiResponse(data={"id": str(attachment.id), "filename": attachment.filename})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/invitees", response_model=ApiResponse)
def select_invitees(id: UUID, supplier_ids: List[UUID], db: Session = Depends(get_db)):
    try:
        invitees = TenderService.select_invitees(db, id, supplier_ids)
        return ApiResponse(data=[TenderInvitee.model_validate(i) for i in invitees])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/publish", response_model=ApiResponse)
async def publish_tender(id: UUID, email_config: dict, db: Session = Depends(get_db)):
    try:
        result = await TenderService.publish_tender(db, id, email_config)
        return ApiResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

