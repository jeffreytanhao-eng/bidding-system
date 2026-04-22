
from typing import List, Dict
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from decimal import Decimal
from src.models.tender import Tender
from src.models.bid import Bid
from src.models.review import Reviewer, ReviewScore
from src.external.email_client import EmailService


class ResultService:
    @staticmethod
    def calculate_summary(db, tender_id):
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        bids = db.query(Bid).filter(Bid.tender_id == tender_id).all()
        reviewers = db.query(Reviewer).filter(Reviewer.tender_id == tender_id).all()
        
        for reviewer in reviewers:
            scores_count = db.query(ReviewScore).filter(ReviewScore.reviewer_id == reviewer.id).count()
            if scores_count < len(bids):
                raise ValueError("存在未完成的评审")
        
        results = []
        business_weight = tender.business_weight or Decimal("0.4")
        technical_weight = tender.technical_weight or Decimal("0.6")
        
        for bid in bids:
            from src.models.supplier import Supplier
            supplier = db.query(Supplier).filter(Supplier.id == bid.supplier_id).first()
            
            business_scores = []
            technical_scores = []
            
            for reviewer in reviewers:
                score = db.query(ReviewScore).filter(
                    ReviewScore.reviewer_id == reviewer.id,
                    ReviewScore.bid_id == bid.id
                ).first()
                
                if score and score.total_score:
                    if reviewer.review_type == "business":
                        business_scores.append(score.total_score)
                    else:
                        technical_scores.append(score.total_score)
            
            business_avg = sum(business_scores) / len(business_scores) if business_scores else Decimal("0")
            technical_avg = sum(technical_scores) / len(technical_scores) if technical_scores else Decimal("0")
            
            weighted_score = (business_avg * business_weight) + (technical_avg * technical_weight)
            
            results.append({
                "bid_id": str(bid.id),
                "supplier_id": str(bid.supplier_id),
                "supplier_name": supplier.name if supplier else "",
                "quote_amount": float(bid.quote_amount) if bid.quote_amount else 0,
                "business_score": float(business_avg),
                "technical_score": float(technical_avg),
                "weighted_score": float(weighted_score)
            })
        
        results.sort(key=lambda x: x["weighted_score"], reverse=True)
        
        for i, r in enumerate(results):
            r["rank"] = i + 1
        
        return results

    @staticmethod
    def set_weights(db, tender_id, business_weight, technical_weight):
        if abs(business_weight + technical_weight - 1.0) > 0.001:
            raise ValueError("权重和必须等于1")
        
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        tender.business_weight = Decimal(str(business_weight))
        tender.technical_weight = Decimal(str(technical_weight))
        db.commit()
        db.refresh(tender)
        return tender

    @staticmethod
    def approve_result(db, tender_id, winner_bid_id, approver_id):
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        bid = db.query(Bid).filter(Bid.id == winner_bid_id).first()
        if not bid:
            raise ValueError("应标不存在")
        
        bid.status = "passed"
        db.commit()
        
        return {
            "tender_id": str(tender_id),
            "winner_bid_id": str(winner_bid_id),
            "winner_supplier_id": str(bid.supplier_id),
            "approved_by": str(approver_id),
            "approved_at": datetime.now().isoformat()
        }

    @staticmethod
    async def announce_result(db, tender_id):
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        from src.models.bid import Bid
        winner_bid = db.query(Bid).filter(
            Bid.tender_id == tender_id,
            Bid.status == "passed"
        ).first()
        
        if not winner_bid:
            raise ValueError("请先审核中标结果")
        
        from src.models.supplier import Supplier
        supplier = db.query(Supplier).filter(Supplier.id == winner_bid.supplier_id).first()
        
        if supplier and supplier.contact_email:
            email_service = EmailService()
            result_info = {
                "tender_title": tender.title,
                "quote_amount": str(winner_bid.quote_amount) if winner_bid.quote_amount else ""
            }
            await email_service.send_winner_notice(supplier.contact_email, result_info)
        
        tender.status = "completed"
        tender.completed_at = datetime.now()
        db.commit()
        
        return {
            "tender_id": str(tender_id),
            "status": tender.status,
            "winner_supplier": supplier.name if supplier else "",
            "announced_at": tender.completed_at.isoformat()
        }
