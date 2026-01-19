from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAccountDTO(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    balance: Decimal = Field(default=Decimal("0.00"))


class ResponseAccountDTO(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    balance: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
