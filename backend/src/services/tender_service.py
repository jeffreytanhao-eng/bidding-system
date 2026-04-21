
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.models.tender import Tender, TenderAttachment, TenderInvitee
from src.schemas.tender import TenderCreate, TenderUpdate
from src.external.email_client import EmailService
import secrets


class TenderService:
    @staticmethod
    def create_tender(db: Session, data: TenderCreate) -&gt; Tender:
        tender = Tender(**data.model_dump())
        db.add(tender)
        db.commit()
        db.refresh(tender)
        return tender

    @staticmethod
    def update_tender(db: Session, tender_id: UUID, data: TenderUpdate) -&gt; Tender:
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tender, key, value)
        
        db.commit()
        db.refresh(tender)
        return tender

    @staticmethod
    def get_tenders(db: Session, status: Optional[str] = None) -&gt; List[Tender]:
        query = db.query(Tender)
        if status:
            query = query.filter(Tender.status == status)
        return query.all()

    @staticmethod
    def get_tender(db: Session, tender_id: UUID) -&gt; Optional[Tender]:
        return db.query(Tender).filter(Tender.id == tender_id).first()

    @staticmethod
    def select_invitees(db: Session, tender_id: UUID, supplier_ids: List[UUID]) -&gt; List[TenderInvitee]:
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        invitees = []
        for supplier_id in supplier_ids:
            existing = db.query(TenderInvitee).filter(
                TenderInvitee.tender_id == tender_id,
                TenderInvitee.supplier_id == supplier_id
            ).first()
            
            if not existing:
                invite_token = secrets.token_urlsafe(32)
                invitee = TenderInvitee(
                    tender_id=tender_id,
                    supplier_id=supplier_id,
                    invite_token=invite_token
                )
                db.add(invitee)
                invitees.append(invitee)
        
        db.commit()
        for invitee in invitees:
            db.refresh(invitee)
        return invitees

    @staticmethod
    async def publish_tender(db: Session, tender_id: UUID, email_config: dict) -&gt; dict:
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        invitees = db.query(TenderInvitee).filter(TenderInvitee.tender_id == tender_id).all()
        if not invitees:
            raise ValueError("请先选择邀请供应商")
        
        email_service = EmailService()
        sent_count = 0
        failed_count = 0
        
        for invitee in invitees:
            from src.models.supplier import Supplier
            supplier = db.query(Supplier).filter(Supplier.id == invitee.supplier_id).first()
            if supplier and supplier.contact_email:
                tender_info = {
                    "title": tender.title,
                    "deadline": tender.deadline.isoformat(),
                    "bid_url": f"/bid-submit/{invitee.invite_token}"
                }
                success = await email_service.send_tender_notice(
                    [supplier.contact_email], tender_info
                )
                if success:
                    invitee.email_sent = True
                    invitee.email_sent_at = datetime.now()
                    sent_count += 1
                else:
                    failed_count += 1
        
        tender.status = "published"
        tender.published_at = datetime.now()
        db.commit()
        
        return {
            "tender_id": str(tender_id),
            "status": tender.status,
            "sent_count": sent_count,
            "failed_count": failed_count,
            "sent_at": tender.published_at.isoformat()
        }

    @staticmethod
    def upload_attachment(db: Session, tender_id: UUID, file: UploadFile) -&gt; TenderAttachment:
        attachment = TenderAttachment(
            tender_id=tender_id,
            filename=file.filename,
            file_path=f"/uploads/{tender_id}/{file.filename}",
            file_size=0,
            file_type=file.content_type
        )
        db.add(attachment)
        db.commit()
        db.refresh(attachment)
        return attachment

