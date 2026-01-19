from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from domain.entities.user import User
from domain.models.user import UserModel as ORMUser
from domain.repositories.user_repository import IUserRepository
from infrastructures.mappers.user_mapper import to_domain, to_orm
from utils.db import async_session_factory


class SQLAlchemyUserRepository(IUserRepository):
    model = ORMUser

    async def save(self, user: User) -> UUID:
        async with async_session_factory() as session:
            orm_user = to_orm(user)
            session.add(orm_user)
            await session.flush()
            await session.commit()
            return orm_user.id

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        async with async_session_factory() as session:
            stmt = (
                select(self.model)
                .where(self.model.id == user_id)
                .options(selectinload(self.model.accounts))
            )
            res = await session.execute(stmt)
            orm_user = res.scalar_one_or_none()
            return to_domain(orm_user) if orm_user else None

    async def get_by_email(self, email: str) -> Optional[User]:
        async with async_session_factory() as session:
            stmt = (
                select(self.model)
                .where(self.model.email == email)
                .options(selectinload(self.model.accounts))
            )
            res = await session.execute(stmt)
            orm_user = res.scalar_one_or_none()
            return to_domain(orm_user) if orm_user else None

    async def delete(self, user_id: UUID) -> bool:
        async with async_session_factory() as session:
            stmt = delete(self.model).where(self.model.id == user_id)
            res = await session.execute(stmt)
            await session.commit()
            return bool(res.rowcount and res.rowcount > 0)  # type: ignore
