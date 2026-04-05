from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from uuid import UUID

from app.db.models import FinancialRecord, TransactionTypeEnum

def get_dashboard_summary(db: Session, owner_id: Optional[UUID] = None):
    query = db.query(
        FinancialRecord.transaction_type,
        func.sum(FinancialRecord.amount).label("total")
    )
    
    if owner_id:
        query = query.filter(FinancialRecord.owner_id == owner_id)
        
    results = query.group_by(FinancialRecord.transaction_type).all()
    
    total_income = 0.0
    total_expenses = 0.0
    
    for row in results:
        if row.transaction_type == TransactionTypeEnum.income:
            total_income = float(row.total) if row.total else 0.0
        elif row.transaction_type == TransactionTypeEnum.expense:
            total_expenses = float(row.total) if row.total else 0.0
            
    net_balance = total_income - total_expenses
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance
    }

def get_category_summary(db: Session, owner_id: Optional[UUID] = None):
    query = db.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount).label("total")
    )
    
    if owner_id:
        query = query.filter(FinancialRecord.owner_id == owner_id)
        
    results = query.group_by(FinancialRecord.category).all()
    
    return [
        {
            "category": row.category, 
            "total_amount": float(row.total) if row.total else 0.0
        } 
        for row in results
    ]