from domain.entities.transaction import Transaction as DomainTransaction
from domain.models.transaction import TransactionModel as ORMTransaction


def to_orm(entity: DomainTransaction) -> ORMTransaction:
    return ORMTransaction(
        id=entity.id,
        user_id=entity.user_id,
        account_id=entity.account_id,
        transaction_type=entity.type,
        amount=entity.amount,
        category_id=entity.category_id,
        date=entity.date,
        description=entity.description,
    )


def to_domain(entity: ORMTransaction) -> DomainTransaction:
    return DomainTransaction(
        id=entity.id,
        user_id=entity.user_id,
        account_id=entity.account_id,
        type=entity.transaction_type,
        amount=entity.amount,
        category_id=entity.category_id,
        date=entity.date,
        description=entity.description,
    )
