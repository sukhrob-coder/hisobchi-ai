from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from .deps import get_current_user
from ..core.database import get_db
from ..models.transaction import Transaction, TransactionType
from ..models.user import User
from ..schemas.user import UserResponse, SummaryResponse

router = APIRouter(tags=["user"])


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = db.query(func.count(Transaction.id)).filter(Transaction.user_id == current_user.id).scalar()
    current_user.transaction_count = count
    return current_user


@router.get("/transactions/summary", response_model=SummaryResponse)
def get_summary(
    from_date: Optional[datetime] = Query(None, alias="from"),
    to_date: Optional[datetime] = Query(None, alias="to"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(
        func.sum(Transaction.amount).filter(Transaction.type == TransactionType.INCOME).label("income"),
        func.sum(Transaction.amount).filter(Transaction.type == TransactionType.EXPENSE).label("expense")
    ).filter(Transaction.user_id == current_user.id)

    if from_date:
        query = query.filter(Transaction.date >= from_date)
    if to_date:
        query = query.filter(Transaction.date <= to_date)

    result = query.one()

    total_income = result.income or 0.0
    total_expense = result.expense or 0.0
    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }
