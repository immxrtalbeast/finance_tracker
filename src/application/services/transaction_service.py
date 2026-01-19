import logging
from datetime import datetime
from decimal import Decimal
from typing import Callable, Optional
from uuid import UUID

from application.services.unit_of_work import IUnitOfWork
from domain.entities.transaction import Transaction, TransactionType
from domain.errors.base_errors import Forbidden, NotFound

logger = logging.getLogger(__name__)


class TransactionService:
    def __init__(self, uow_factory: Callable[[], IUnitOfWork]):
        self.uow_factory = uow_factory

    async def save(
        self,
        current_uid: UUID,
        account_id: UUID,
        category_id: Optional[UUID],
        amount: Decimal,
        type: TransactionType,
        description: Optional[str],
        date: Optional[datetime],
    ) -> UUID:
        op = "transaction.service.save"
        logger.info(
            f"saving transaction, op={op}, account_id={account_id}, amount={amount}, type={type}"
        )
        async with self.uow_factory() as uow:
            account = await uow.accounts.get_by_id(account_id)
            if account is None:
                logger.warning(
                    f"account doesn`t exist op={op}, account_id={account_id}, amount={amount}, type={type}"
                )
                raise NotFound("Account", str(account_id))
            if account.user_id != current_uid:
                logger.warning(
                    f"account doesn`t belong to user, op={op}, account_id={account_id}"
                )
                raise Forbidden("Account", str(account_id))

            await uow.accounts.update_balance(account.id, amount)
            tx = Transaction(
                user_id=current_uid,
                account_id=account_id,
                category_id=category_id,
                amount=amount,
                type=type,
                date=date,
                description=description,
            )
            tx_id = await uow.transactions.save(tx)
            logger.info(
                f"transaction saved, op={op}, transaction_id={tx_id}, account_id={account_id}, amount={amount}, type={type}"
            )
            return tx_id

    async def by_id(self, transaction_id: UUID, current_uid: UUID):
        op = "transaction.service.by_id"
        logger.info(f"getting transaction, op={op}, transaction_id={transaction_id}")
        async with self.uow_factory() as uow:
            tx = await uow.transactions.get_transaction_by_id(transaction_id)
            if tx == None:
                logger.warning(
                    f"transaction not found, op={op}, transaction_id={transaction_id}"
                )
                raise NotFound("Transaction", str(transaction_id))
            if tx.user_id != current_uid:
                logger.warning(
                    f"transaction doesn`t belongs to user, op={op}, transaction_id={transaction_id}"
                )
                raise Forbidden("Transaction", str(transaction_id))
            logger.info(f"transaction getted, op={op}, transaction_id={transaction_id}")
            return tx

    async def delete(self, transaction_id: UUID, current_uid: UUID):
        op = "transaction.service.delete"
        logger.info(f"deleting transaction, op={op}, transaction_id={transaction_id}")
        async with self.uow_factory() as uow:
            tx = await uow.transactions.get_transaction_by_id(transaction_id)
            if tx == None:
                logger.warning(
                    f"transaction not found, op={op}, transaction_id={transaction_id}"
                )
                raise NotFound("Transaction", str(transaction_id))
            if tx.user_id != current_uid:
                logger.warning(
                    f"transaction doesn`t belongs to user, op={op}, transaction_id={transaction_id}"
                )
                raise Forbidden("Transaction", str(transaction_id))
            res = await uow.transactions.delete(transaction_id)
            logger.info(
                f"transaction deleted, op={op}, transaction_id={transaction_id}"
            )
            return res

    async def get_account_transactions(self, account_id: UUID, current_uid: UUID):
        op = "transaction.service.get_account_transactions"
        logger.info(f"getting account transactions, op={op}, account_id={account_id}")
        async with self.uow_factory() as uow:
            account = await uow.accounts.get_by_id(account_id)
            if account == None:
                logger.warning(f"account not found, op={op}, account_id={account_id}")
                raise NotFound("Account", str(account_id))
            if account.user_id != current_uid:
                logger.warning(
                    f"account doesn`t belong to user, op={op}, account_id={account_id}"
                )
                raise Forbidden("Account", str(account_id))
            tx = await uow.transactions.get_account_transactions(account_id)
            logger.info(f"account transactions getted op={op}, account_id={account_id}")
            return tx
