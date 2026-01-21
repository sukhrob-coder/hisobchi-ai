from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.transaction import TariffType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tariff = Column(String, default=TariffType.FREE)
    chatID = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True, unique=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("Transaction", back_populates="owner")
