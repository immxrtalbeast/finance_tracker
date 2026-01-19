from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from application.dto.account import CreateAccountDTO, ResponseAccountDTO
from application.services.account_service import AccountService
from presentation.api.dependencies import account_service, current_user_id

router = APIRouter(prefix="/accounts", tags=["Accounts💳"])


@router.post("")
async def save_account(
    accountDTO: CreateAccountDTO,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[AccountService, Depends(account_service)],
):
    account_id = await service.save(
        user_id=current_uid, name=accountDTO.name, balance=accountDTO.balance
    )
    return {"account_id": account_id}


@router.get("/{account_id}", response_model=ResponseAccountDTO)
async def account(
    account_id: UUID,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[AccountService, Depends(account_service)],
):
    account = await service.by_id(account_id, current_uid)
    return account


@router.delete("/{account_id}")
async def delete(
    account_id: UUID,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[AccountService, Depends(account_service)],
):
    res = await service.delete(account_id, current_uid)
    return {"status": res}


@router.patch("/{account_id}")
async def update_balance(
    account_id: UUID,
    amount: Decimal,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[AccountService, Depends(account_service)],
):
    res = await service.update_balance(account_id, amount, current_uid)
    return {"status": res}


@router.get("/user/{user_id}", response_model=list[ResponseAccountDTO])
async def user_accounts(
    user_id: UUID,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[AccountService, Depends(account_service)],
):
    accounts = await service.get_user_accounts(user_id, current_uid)
    return accounts
