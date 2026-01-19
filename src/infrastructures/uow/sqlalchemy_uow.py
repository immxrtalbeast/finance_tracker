from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from application.services.unit_of_work import IUnitOfWork
from domain.repositories.account_repository import IAccountRepository
from domain.repositories.transaction_repository import ITransactionRepository
from infrastructures.db.account_db import SQLAlchemyAccountRepository
from infrastructures.db.transaction_db import SQLAlchemyTransactionRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    accounts: IAccountRepository
    transactions: ITransactionRepository

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.accounts = SQLAlchemyAccountRepository(self.session)
        self.transactions = SQLAlchemyTransactionRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        if self.session:
            await self.session.close()

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
