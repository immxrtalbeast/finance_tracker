from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionTypeDTO(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class TransactionCreateDTO(BaseModel):
    account_id: UUID
    category_id: Optional[UUID] = None
    amount: Decimal
    type: TransactionTypeDTO
    description: Optional[str] = None
    date: Optional[datetime] = None


class TransactionResponseDTO(BaseModel):
    id: UUID
    account_id: UUID
    category_id: Optional[UUID]
    amount: Decimal
    type: str
    description: Optional[str]
    date: datetime

    class Config:
        from_attributes = True
