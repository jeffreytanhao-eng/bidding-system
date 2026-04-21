
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from src.models.review import Reviewer, ReviewScore
from src.schemas.review import ScoreCreate
from src.external.dingtalk_client import DingTalkService
from decimal import Decimal


class ReviewService:
    @staticmethod
    def assign_reviewers(db, tender_id, reviewers):
        from src.models.tender import Tender
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        assigned_reviewers = []
        for r in reviewers:
            existing = db.query(Reviewer).filter(
                Reviewer.tender_id == tender_id,
                Reviewer.user_id == UUID(r["user_id"]),
                Reviewer.review_type == r["review_type"]
            ).first()
            
            if not existing:
                reviewer = Reviewer(
                    tender_id=tender_id,
                    user_id=UUID(r["user_id"]),
                    dingtalk_user_id=r.get("dingtalk_user_id"),
                    review_type=r["review_type"]
                )
                db.add(reviewer)
                assigned_reviewers.append(reviewer)
        
        db.commit()
        for reviewer in assigned_reviewers:
            db.refresh(reviewer)
        return assigned_reviewers

    @staticmethod
    async def start_review(db, tender_id):
        from src.models.tender import Tender
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            raise ValueError("标书不存在")
        
        reviewers = db.query(Reviewer).filter(Reviewer.tender_id == tender_id).all()
        if not reviewers:
            raise ValueError("请先指派评审人员")
        
        dingtalk_service = DingTalkService()
        notified_count = 0
        
        for reviewer in reviewers:
            if reviewer.dingtalk_user_id:
                message = {
                    "msgtype": "text",
                    "text": {
                        "content": f"您有新的评审任务：{tender.title}，请及时完成评审。"
                    }
                }
                try:
                    await dingtalk_service.send_work_notice(reviewer.dingtalk_user_id, message)
                    reviewer.status = "notified"
                    notified_count += 1
                except Exception:
                    pass
        
        tender.status = "reviewing"
        db.commit()
        
        return {
            "tender_id": str(tender_id),
            "status": tender.status,
            "reviewer_count": len(reviewers),
            "notified_count": notified_count
        }

    @staticmethod
    def submit_score(db, reviewer_id, bid_id, score_data):
        reviewer = db.query(Reviewer).filter(Reviewer.id == reviewer_id).first()
        if not reviewer:
            raise ValueError("评审人员不存在")
        
        existing = db.query(ReviewScore).filter(
            ReviewScore.reviewer_id == reviewer_id,
            ReviewScore.bid_id == bid_id
        ).first()
        
        if existing:
            for key, value in score_data.model_dump(exclude_unset=True).items():
                setattr(existing, key, value)
            
            if existing.price_score and existing.qualification_score and existing.experience_score and existing.service_score:
                total = (existing.price_score + existing.qualification_score + 
                         existing.experience_score + existing.service_score) / 4
                existing.total_score = Decimal(str(round(total, 2)))
            
            db.commit()
            db.refresh(existing)
            return existing
        
        total_score = None
        if (score_data.price_score and score_data.qualification_score and 
            score_data.experience_score and score_data.service_score):
            total = (score_data.price_score + score_data.qualification_score + 
                     score_data.experience_score + score_data.service_score) / 4
            total_score = Decimal(str(round(total, 2)))
        
        review_score = ReviewScore(
            reviewer_id=reviewer_id,
            bid_id=bid_id,
            price_score=score_data.price_score,
            qualification_score=score_data.qualification_score,
            experience_score=score_data.experience_score,
            service_score=score_data.service_score,
            total_score=total_score,
            comment=score_data.comment,
            recommendation=score_data.recommendation
        )
        db.add(review_score)
        db.commit()
        db.refresh(review_score)
        
        reviewer.status = "in_progress"
        db.commit()
        
        return review_score

    @staticmethod
    def get_review_progress(db, tender_id):
        reviewers = db.query(Reviewer).filter(Reviewer.tender_id == tender_id).all()
        
        from src.models.bid import Bid
        bids = db.query(Bid).filter(Bid.tender_id == tender_id).all()
        
        total_reviewers = len(reviewers)
        completed_count = 0
        in_progress_count = 0
        
        for reviewer in reviewers:
            scores_count = db.query(ReviewScore).filter(
                ReviewScore.reviewer_id == reviewer.id
            ).count()
            
            if scores_count &gt;= len(bids):
                completed_count += 1
            elif scores_count &gt; 0:
                in_progress_count += 1
        
        return {
            "tender_id": str(tender_id),
            "total_reviewers": total_reviewers,
            "completed_count": completed_count,
            "in_progress_count": in_progress_count,
            "pending_count": total_reviewers - completed_count - in_progress_count
        }

    @staticmethod
    async def remind_reviewers(db, tender_id):
        reviewers = db.query(Reviewer).filter(
            Reviewer.tender_id == tender_id,
            Reviewer.status != "completed"
        ).all()
        
        dingtalk_service = DingTalkService()
        reminded_count = 0
        
        for reviewer in reviewers:
            if reviewer.dingtalk_user_id:
                message = {
                    "msgtype": "text",
                    "text": {
                        "content": "【催办提醒】您还有未完成的评审任务，请及时完成！"
                    }
                }
                try:
                    await dingtalk_service.send_work_notice(reviewer.dingtalk_user_id, message)
                    reminded_count += 1
                except Exception:
                    pass
        
        return reminded_count
