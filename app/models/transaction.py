from enum import Enum

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TariffType(str, Enum):
    FREE = "FREE"
    PRO = "PRO"


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="transactions")
