import logging
from uuid import UUID

from passlib.context import CryptContext

from domain.entities.user import User
from domain.errors.base_errors import NotFound
from domain.errors.user_errors import InvalidCredentials, UserAlreadyExists
from domain.repositories.user_repository import IUserRepository
from utils import jwt_util

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["argon2"])


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo: IUserRepository = user_repo

    async def save_user(self, email: str, raw_password: str):
        op = "user.service.save"
        logger.info(f"creating user, op={op}, email={email}")
        if await self.user_repo.get_by_email(email) != None:
            logger.warning(f"user exists, op={op}, email={email}")
            raise UserAlreadyExists(email)
        hash_pass = pwd_context.hash(raw_password)
        user = User(email=email, hashed_password=hash_pass)
        user_id = await self.user_repo.save(user=user)
        logger.info(f"user created, op={op}, email={email}, id={user_id}")
        return user_id

    async def get_user_by_id(self, id: UUID):
        op = "user.service.get_by_id"
        logger.info(f"getting user, op={op}, id={id}")
        user = await self.user_repo.get_by_id(id)
        if user == None:
            logger.warning(f"user doesn`t exists, op={op}, id={id}")
            raise NotFound("User", str(id))
        logger.info(f"user getted, op={op}, id={id}")
        return user

    async def delete(self, id: UUID):
        op = "user.service.delete"
        logger.info(f"deleting user, op={op}, id={id}")
        user = await self.user_repo.get_by_id(id)
        if user == None:
            logger.warning(f"user doesn`t exists, op={op}, id={id}")
            raise NotFound("User", str(id))
        res = await self.user_repo.delete(id)
        return res

    async def get_user_by_email(self, email: str):
        op = "user.service.get_by_email"
        logger.info(f"getting user, op={op}, email={email}")
        user = await self.user_repo.get_by_email(email)
        if user == None:
            logger.warning(f"user doesn`t exists, op={op}, email={email}")
            raise NotFound("User", str(email))
        logger.info(f"user getted, op={op}, email={email}")
        return user

    async def login(self, email: str, raw_password: str):
        op = "user.service.login"
        logger.info(f"trying to login, op={op}, email={email}")
        user = await self.user_repo.get_by_email(email)
        if user == None:
            raise InvalidCredentials()
        if pwd_context.verify(raw_password, user.hashed_password):
            logger.info(f"login success, op={op}, email={email}")
            return jwt_util.create_access_token(
                {"sub": str(user.id), "email": user.email}
            )
        else:
            logger.warning(f"invalid credentials, op={op}, email={email}")
            raise InvalidCredentials()
