
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.supplier import Supplier, SupplierTag
from src.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    @staticmethod
    def create_supplier(db: Session, data: SupplierCreate) -&gt; Supplier:
        supplier = Supplier(**data.model_dump())
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def update_supplier(db: Session, supplier_id: UUID, data: SupplierUpdate) -&gt; Supplier:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise ValueError("供应商不存在")
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(supplier, key, value)
        
        db.commit()
        db.refresh(supplier)
        return supplier

    @staticmethod
    def get_suppliers(db: Session, filters: Optional[dict] = None) -&gt; List[Supplier]:
        query = db.query(Supplier)
        
        if filters:
            if filters.get("rating"):
                query = query.filter(Supplier.rating == filters["rating"])
            if filters.get("status"):
                query = query.filter(Supplier.status == filters["status"])
            if filters.get("name"):
                query = query.filter(Supplier.name.contains(filters["name"]))
        
        return query.all()

    @staticmethod
    def get_supplier(db: Session, supplier_id: UUID) -&gt; Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.id == supplier_id).first()

    @staticmethod
    def add_tag(db: Session, supplier_id: UUID, tag_name: str) -&gt; SupplierTag:
        tag = db.query(SupplierTag).filter(SupplierTag.name == tag_name).first()
        if not tag:
            tag = SupplierTag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        return tag

    @staticmethod
    def update_rating(db: Session, supplier_id: UUID, rating: str) -&gt; Supplier:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise ValueError("供应商不存在")
        supplier.rating = rating
        db.commit()
        db.refresh(supplier)
        return supplier

