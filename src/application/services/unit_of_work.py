from abc import ABC
from typing import Self

from domain.repositories.account_repository import IAccountRepository
from domain.repositories.transaction_repository import ITransactionRepository


class IUnitOfWork(ABC):
    accounts: IAccountRepository
    transactions: ITransactionRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
