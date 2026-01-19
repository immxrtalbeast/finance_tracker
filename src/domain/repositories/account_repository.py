from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from domain.entities.account import Account


class IAccountRepository(ABC):
    @abstractmethod
    async def get_by_id(self, account_id: UUID) -> Optional[Account]:
        pass

    @abstractmethod
    async def get_user_accounts(self, user_id: UUID) -> List[Account]:
        pass

    @abstractmethod
    async def save(self, account: Account) -> UUID:
        pass

    @abstractmethod
    async def delete(self, account_id: UUID) -> bool:
        pass

    @abstractmethod
    async def update_balance(self, account_id: UUID, amount: Decimal) -> bool:
        pass
