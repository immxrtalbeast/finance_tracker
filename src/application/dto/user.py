from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from application.dto.account import ResponseAccountDTO


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=30)


class UserLoginDTO(UserCreateDTO):
    pass


class UserResponseDTO(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime
    accounts: List[ResponseAccountDTO]

    class Config:
        from_attributes = True


class UserByEmailDTO(BaseModel):
    email: EmailStr
