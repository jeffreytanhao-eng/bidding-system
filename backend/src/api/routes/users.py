
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.models.user import User
from src.schemas.common import ApiResponse
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(tags=["用户管理"])


class UserCreate(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None
    role: str = "reviewer"


@router.post("/users", response_model=ApiResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    user = User(
        id=uuid.uuid4(),
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        role=user_data.role,
        status="active"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return ApiResponse(data={
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "status": user.status
    })


@router.get("/users", response_model=ApiResponse)
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return ApiResponse(data=[{
        "id": str(u.id),
        "username": u.username,
        "email": u.email,
        "phone": u.phone,
        "role": u.role,
        "status": u.status,
        "created_at": str(u.created_at) if u.created_at else None
    } for u in users])


@router.get("/users/{user_id}", response_model=ApiResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return ApiResponse(data={
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "status": user.status
    })
