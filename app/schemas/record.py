from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.db.models import TransactionTypeEnum

class FinancialRecordCreate(BaseModel):
    amount: float = Field(..., gt=0)
    transaction_type: TransactionTypeEnum
    category: str = Field(..., min_length=1)
    transaction_date: Optional[datetime] = None  # If none, serverside assigns current
    notes: Optional[str] = None
    owner_id: UUID

class FinancialRecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    transaction_type: Optional[TransactionTypeEnum] = None
    category: Optional[str] = Field(None, min_length=1)
    transaction_date: Optional[datetime] = None
    notes: Optional[str] = None

class FinancialRecordResponse(BaseModel):
    id: UUID
    owner_id: UUID
    amount: float
    transaction_type: TransactionTypeEnum
    category: str
    transaction_date: datetime
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Summaries DTOs
class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float

class CategorySummary(BaseModel):
    category: str
    total_amount: float
