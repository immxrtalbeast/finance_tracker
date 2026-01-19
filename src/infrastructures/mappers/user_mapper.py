from domain.entities.user import User as DomainUser
from domain.models.user import UserModel as ORMUser
from infrastructures.mappers.account_mapper import to_domain as to_domain_acc


def to_orm(entity: DomainUser) -> ORMUser:
    return ORMUser(
        id=entity.id,
        email=entity.email,
        hashed_password=entity.hashed_password,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def to_domain(entity: ORMUser) -> DomainUser:
    accounts_raw = entity.__dict__.get("accounts")
    return DomainUser(
        id=entity.id,
        email=entity.email,
        hashed_password=entity.hashed_password,
        accounts=[to_domain_acc(x) for x in accounts_raw] if accounts_raw else [],
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
