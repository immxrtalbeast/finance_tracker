from domain.entities.account import Account as DomainAccount
from domain.models.account import AccountModel as ORMAccount
from infrastructures.mappers.transaction_mapper import to_domain as to_domain_trans


def to_orm(entity: DomainAccount) -> ORMAccount:
    return ORMAccount(
        id=entity.id,
        user_id=entity.user_id,
        name=entity.name,
        balance=entity.balance,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def to_domain(entity: ORMAccount) -> DomainAccount:
    transactions_raw = entity.__dict__.get("transactions")

    return DomainAccount(
        id=entity.id,
        user_id=entity.user_id,
        name=entity.name,
        balance=entity.balance,
        transactions=(
            [to_domain_trans(x) for x in transactions_raw] if transactions_raw else []
        ),
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
