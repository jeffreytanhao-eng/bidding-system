
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.models.bid import Bid, BidFile
from src.models.tender import TenderInvitee
from src.schemas.bid import BidCreate


class BidService:
    @staticmethod
    def validate_invite_token(db: Session, token: str) -&gt; Optional[TenderInvitee]:
        return db.query(TenderInvitee).filter(TenderInvitee.invite_token == token).first()

    @staticmethod
    def submit_bid(db: Session, invite_token: str, data: BidCreate) -&gt; Bid:
        invitee = db.query(TenderInvitee).filter(TenderInvitee.invite_token == invite_token).first()
        if not invitee:
            raise ValueError("无效的应标令牌")
        
        from src.models.tender import Tender
        tender = db.query(Tender).filter(Tender.id == invitee.tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        if datetime.now() &gt; tender.deadline:
            raise ValueError("已超过应标截止时间")
        
        existing_bid = db.query(Bid).filter(
            Bid.tender_id == invitee.tender_id,
            Bid.supplier_id == invitee.supplier_id
        ).first()
        
        if existing_bid:
            raise ValueError("您已提交过应标")
        
        bid = Bid(
            tender_id=invitee.tender_id,
            supplier_id=invitee.supplier_id,
            quote_amount=data.quote_amount,
            delivery_period=data.delivery_period,
            contact_person=data.contact_person,
            contact_phone=data.contact_phone,
            technical_summary=data.technical_summary
        )
        db.add(bid)
        db.commit()
        db.refresh(bid)
        return bid

    @staticmethod
    def upload_bid_file(db: Session, bid_id: UUID, file: UploadFile, file_type: str) -&gt; BidFile:
        bid_file = BidFile(
            bid_id=bid_id,
            type=file_type,
            filename=file.filename,
            file_path=f"/uploads/bids/{bid_id}/{file_type}/{file.filename}",
            file_size=0,
            file_type=file.content_type
        )
        db.add(bid_file)
        db.commit()
        db.refresh(bid_file)
        return bid_file

    @staticmethod
    def get_bids_by_tender(db: Session, tender_id: UUID) -&gt; List[Bid]:
        return db.query(Bid).filter(Bid.tender_id == tender_id).all()

    @staticmethod
    def get_bid(db: Session, bid_id: UUID) -&gt; Optional[Bid]:
        return db.query(Bid).filter(Bid.id == bid_id).first()

