from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

from ..models.transaction import TariffType


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    tariff: TariffType
    chatID: Optional[str] = None
    telegram_id: Optional[str] = None
    created_at: datetime
    transaction_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float
