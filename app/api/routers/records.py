from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from uuid import UUID

from app.db.database import get_db
from app.db.models import FinancialRecord, User, TransactionTypeEnum
from app.schemas.record import FinancialRecordCreate, FinancialRecordUpdate, FinancialRecordResponse, DashboardSummary, CategorySummary
from app.api.dependencies import get_current_active_user, require_admin, require_analyst_or_admin
from app.services import record_service

router = APIRouter()

@router.post("/", response_model=FinancialRecordResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_record(
    record_in: FinancialRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new financial record.
    """
    new_record = FinancialRecord(
        owner_id=record_in.owner_id,
        amount=record_in.amount,
        transaction_type=record_in.transaction_type,
        category=record_in.category,
        transaction_date=record_in.transaction_date,
        notes=record_in.notes
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/", response_model=List[FinancialRecordResponse])
def get_records(
    skip: int = 0,
    limit: int = 100,
    transaction_type: Optional[TransactionTypeEnum] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve financial records with optional filters.
    """
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date"
        )

    query = db.query(FinancialRecord)
    
    if transaction_type:
        query = query.filter(FinancialRecord.transaction_type == transaction_type)
    if category:
        query = query.filter(FinancialRecord.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(FinancialRecord.transaction_date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.transaction_date <= end_date)
        
    records = query.offset(skip).limit(limit).all()
    return records

@router.get("/summary", response_model=DashboardSummary, dependencies=[Depends(require_analyst_or_admin)])
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin)
):
    """
    Get overall financial summary (total income, expenses, and net balance).
    """
    # Assuming admins/analysts can see the global summary.
    # If it should be per-user, pass `current_user.id` to `get_dashboard_summary`.
    return record_service.get_dashboard_summary(db)

@router.get("/summary/category", response_model=List[CategorySummary], dependencies=[Depends(require_analyst_or_admin)])
def get_category_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin)
):
    """
    Get category-wise financial summary.
    """
    return record_service.get_category_summary(db)

@router.put("/{record_id}", response_model=FinancialRecordResponse, dependencies=[Depends(require_admin)])
def update_record(
    record_id: UUID,
    record_in: FinancialRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update a financial record by ID.
    """
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
        
    update_data = record_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
        
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_record(
    record_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a financial record by ID.
    """
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
        
    db.delete(record)
    db.commit()
    return None