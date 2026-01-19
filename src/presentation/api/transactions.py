from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from application.dto.transaction import TransactionCreateDTO, TransactionResponseDTO
from application.services.transaction_service import TransactionService
from domain.entities.transaction import TransactionType
from presentation.api.dependencies import current_user_id, transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions💵"])


@router.post("")
async def save_transaction(
    dto: TransactionCreateDTO,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[TransactionService, Depends(transaction_service)],
):
    transaction_id = await service.save(
        current_uid,
        dto.account_id,
        dto.category_id,
        dto.amount,
        TransactionType(dto.type.value),
        dto.description,
        dto.date,
    )
    return {"transaction_id": transaction_id}


@router.get("/{transaction_id}", response_model=TransactionResponseDTO)
async def account(
    transaction_id: UUID,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[TransactionService, Depends(transaction_service)],
):
    account = await service.by_id(transaction_id, current_uid)
    return account


@router.delete("/{account_id}")
async def delete(
    transaction_id: UUID,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[TransactionService, Depends(transaction_service)],
):
    res = await service.delete(transaction_id, current_uid)
    return {"status": res}


@router.get("/account/{account_id}", response_model=list[TransactionResponseDTO])
async def user_transactions(
    account_id: UUID,
    current_uid: Annotated[UUID, Depends(current_user_id)],
    service: Annotated[TransactionService, Depends(transaction_service)],
):
    transactions = await service.get_account_transactions(account_id, current_uid)
    return transactions
