from decimal import Decimal
from typing import List
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.account import Account
from domain.models.account import AccountModel as ORMAccount
from domain.repositories.account_repository import IAccountRepository
from infrastructures.mappers.account_mapper import to_domain, to_orm


class SQLAlchemyAccountRepository(IAccountRepository):
    model = ORMAccount

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, account: Account) -> UUID:
        orm_account = to_orm(account)
        self.session.add(orm_account)
        await self.session.flush()
        await self.session.commit()
        return orm_account.id

    async def get_by_id(self, account_id: UUID) -> Account | None:

        stmt = (
            select(self.model)
            .where(self.model.id == account_id)
            .options(selectinload(self.model.transactions))
        )
        res = await self.session.execute(stmt)
        orm_account = res.scalar_one_or_none()
        return to_domain(orm_account) if orm_account else None

    async def delete(self, account_id: UUID) -> bool:
        stmt = delete(self.model).where(self.model.id == account_id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return bool(res.rowcount and res.rowcount > 0)  # type: ignore

    async def get_user_accounts(self, user_id: UUID) -> List[Account]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        res = await self.session.execute(stmt)
        orm_account_list = res.scalars().all()
        return [to_domain(account) for account in orm_account_list]

    async def update_balance(self, account_id: UUID, amount: Decimal) -> bool:
        stmt = (
            update(self.model)
            .where(self.model.id == account_id)
            .values(balance=self.model.balance + amount)
        )
        res = await self.session.execute(stmt)
        await self.session.commit()
        return bool(res.rowcount and res.rowcount > 0)  # type: ignore
