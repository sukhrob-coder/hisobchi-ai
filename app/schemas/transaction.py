from pydantic import BaseModel
from typing import Optional

from ..models import TransactionType


class TransactionBase(BaseModel):
    amount: float
    type: TransactionType
    category: str
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    date: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
