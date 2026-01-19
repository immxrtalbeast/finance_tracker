from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.transaction import Transaction


class ITransactionRepository(ABC):
    @abstractmethod
    async def save(self, transaction: Transaction) -> UUID:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    async def get_account_transactions(self, account_id: UUID) -> List[Transaction]:
        pass

    @abstractmethod
    async def get_transaction_by_id(self, id: UUID) -> Optional[Transaction]:
        pass
