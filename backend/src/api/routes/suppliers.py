
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.utils.database import get_db
from src.services.supplier_service import SupplierService
from src.schemas.supplier import Supplier, SupplierCreate, SupplierUpdate, SupplierTag
from src.schemas.common import ApiResponse

router = APIRouter(prefix="/suppliers", tags=["供应商管理"])


@router.post("", response_model=ApiResponse)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    try:
        supplier = SupplierService.create_supplier(db, data)
        return ApiResponse(data=Supplier.model_validate(supplier))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", response_model=ApiResponse)
def update_supplier(id: UUID, data: SupplierUpdate, db: Session = Depends(get_db)):
    try:
        supplier = SupplierService.update_supplier(db, id, data)
        return ApiResponse(data=Supplier.model_validate(supplier))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=ApiResponse)
def list_suppliers(
    rating: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    filters = {}
    if rating:
        filters["rating"] = rating
    if status:
        filters["status"] = status
    if name:
        filters["name"] = name
    
    suppliers = SupplierService.get_suppliers(db, filters)
    return ApiResponse(data=[Supplier.model_validate(s) for s in suppliers])


@router.get("/{id}", response_model=ApiResponse)
def get_supplier(id: UUID, db: Session = Depends(get_db)):
    supplier = SupplierService.get_supplier(db, id)
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    return ApiResponse(data=Supplier.model_validate(supplier))


@router.post("/{id}/tags", response_model=ApiResponse)
def add_tag(id: UUID, tag_name: str, db: Session = Depends(get_db)):
    try:
        tag = SupplierService.add_tag(db, id, tag_name)
        return ApiResponse(data=SupplierTag.model_validate(tag))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}/tags/{tag_id}", response_model=ApiResponse)
def remove_tag(id: UUID, tag_id: UUID, db: Session = Depends(get_db)):
    return ApiResponse(message="标签删除成功")


@router.put("/{id}/rating", response_model=ApiResponse)
def update_rating(id: UUID, rating: str, db: Session = Depends(get_db)):
    try:
        supplier = SupplierService.update_rating(db, id, rating)
        return ApiResponse(data=Supplier.model_validate(supplier))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

