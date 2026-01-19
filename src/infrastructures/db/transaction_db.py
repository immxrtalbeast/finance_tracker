from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.transaction import Transaction
from domain.models.transaction import TransactionModel as ORMTransaction
from domain.repositories.transaction_repository import ITransactionRepository
from infrastructures.mappers.transaction_mapper import to_domain, to_orm


class SQLAlchemyTransactionRepository(ITransactionRepository):
    model = ORMTransaction

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, transaction: Transaction) -> UUID:
        orm_transaction = to_orm(transaction)
        self.session.add(orm_transaction)
        await self.session.flush()
        return orm_transaction.id

    async def get_transaction_by_id(self, id: UUID) -> Optional[Transaction]:
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        orm_transaction = res.scalar_one_or_none()
        return to_domain(orm_transaction) if orm_transaction else None

    async def get_account_transactions(self, account_id: UUID) -> List[Transaction]:
        stmt = select(self.model).where(self.model.account_id == account_id)
        res = await self.session.execute(stmt)
        orm_transactions_list = res.scalars().all()
        return [to_domain(transaction) for transaction in orm_transactions_list]

    async def delete(self, id: UUID) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        return bool(res.rowcount and res.rowcount > 0)  # type: ignore
