import logging
from decimal import Decimal
from uuid import UUID

from domain.entities.account import Account
from domain.errors.base_errors import Forbidden, NotFound
from domain.repositories.account_repository import IAccountRepository
from domain.repositories.user_repository import IUserRepository

logger = logging.getLogger(__name__)


class AccountService:
    def __init__(self, account_repo: IAccountRepository, user_repo: IUserRepository):
        self.account_repo: IAccountRepository = account_repo
        self.user_repo: IUserRepository = user_repo

    async def save(self, user_id: UUID, name: str, balance: Decimal):
        op = "account.service.save"
        logger.info(
            f"saving account, op={op}, user_id={user_id}, name={name}, balance={balance}"
        )
        user = await self.user_repo.get_by_id(user_id)
        if user == None:
            logger.warning(
                f"user doesn`t exists op={op}, user_id={user_id}, name={name}, balance={balance}"
            )
            raise NotFound("User", str(user_id))
        account = Account(user_id=user_id, name=name, balance=balance)
        account_id = await self.account_repo.save(account)
        logger.info(
            f"account saved, op={op}, account_id={account_id},user_id={user_id}, name={name}, balance={balance}"
        )
        return account_id

    async def by_id(self, account_id: UUID, current_uid: UUID):
        op = "account.service.by_id"
        logger.info(f"getting account, op={op}, account_id={account_id}")
        account = await self.account_repo.get_by_id(account_id)
        if account == None:
            logger.warning(f"account not found, op={op}, account_id={account_id}")
            raise NotFound("Account", str(account_id))
        if account.user_id != current_uid:
            logger.warning(
                f"account doesn`t belongs to user, op={op}, account_id={account_id}"
            )
            raise Forbidden("Account", str(account_id))
        logger.info(f"account getted, op={op}, account_id={account_id}")
        return account

    async def delete(self, account_id: UUID, current_uid: UUID):
        op = "account.service.delete"
        logger.info(f"deleting account, op={op}, account_id={account_id}")
        account = await self.account_repo.get_by_id(account_id)
        if account == None:
            logger.warning(f"account not found, op={op}, account_id={account_id}")
            raise NotFound("Account", str(account_id))
        if account.user_id != current_uid:
            logger.warning(
                f"account doesn`t belongs to user, op={op}, account_id={account_id}"
            )
            raise Forbidden("Account", str(account_id))
        res = await self.account_repo.delete(account_id)
        logger.info(f"account deleted, op={op}, account_id={account_id}")
        return res

    async def update_balance(
        self, account_id: UUID, amount: Decimal, current_uid: UUID
    ):
        op = "account.service.update_balance"
        logger.info(
            f"updating account balance, op={op}, account_id={account_id}, amount={amount}"
        )
        account = await self.account_repo.get_by_id(account_id)
        if account == None:
            logger.warning(f"account not found, op={op}, account_id={account_id}")
            raise NotFound("Account", str(account_id))
        if account.user_id != current_uid:
            logger.warning(
                f"account doesn`t belongs to user, op={op}, account_id={account_id}"
            )
            raise Forbidden("Account", str(account_id))
        res = await self.account_repo.update_balance(account_id, amount)
        logger.info(
            f"account balance updated, op={op}, account_id={account_id}, amount={amount}"
        )
        return res

    async def get_user_accounts(self, user_id: UUID, current_uid: UUID):
        op = "account.service.get_user_accounts"
        logger.info(f"getting user accounts, op={op}, user_id={user_id}")
        if user_id != current_uid:
            logger.warning(f"forbidden source, op={op}, user_id={user_id}")
            raise Forbidden("User", str(user_id))
        user = await self.user_repo.get_by_id(user_id)
        if user == None:
            logger.warning(f"user not found, op={op}, user_id={user_id}")
            raise NotFound("User", str(user_id))
        accounts = await self.account_repo.get_user_accounts(user_id)
        logger.info(f"user accounts getted op={op}, user_id={user_id}")
        return accounts
