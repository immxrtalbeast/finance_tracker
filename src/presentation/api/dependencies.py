from uuid import UUID

from fastapi import Depends, HTTPException, Request, status

from application.services.account_service import AccountService
from application.services.transaction_service import TransactionService
from application.services.user_service import UserService
from infrastructures.db.account_db import SQLAlchemyAccountRepository
from infrastructures.db.user_db import SQLAlchemyUserRepository
from infrastructures.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from utils import jwt_util
from utils.db import async_session_factory


def uow():
    return SQLAlchemyUnitOfWork(async_session_factory)


def user_service():
    return UserService(SQLAlchemyUserRepository())


async def account_repo():
    async with async_session_factory() as session:
        yield SQLAlchemyAccountRepository(session)


def account_service(
    repo=Depends(account_repo),
):
    return AccountService(repo, SQLAlchemyUserRepository())


def transaction_service():
    return TransactionService(uow)


async def current_user_id(req: Request) -> UUID:
    token = req.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    payload = jwt_util.decode_token(token)
    return UUID(payload["sub"])
