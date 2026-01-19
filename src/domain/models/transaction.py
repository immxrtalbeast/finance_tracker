import uuid
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum

from domain.entities.transaction import TransactionType as TypeENUM
from utils.db import Base

TransactionType = Enum(
    TypeENUM,
    name="transaction_type",
    values_callable=lambda obj: [item.value for item in obj],
)


class TransactionModel(Base):
    __tablename__ = "transactions"
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2, asdecimal=True), default=Decimal("0.00"), nullable=False
    )
    transaction_type: Mapped[TypeENUM] = mapped_column(TransactionType, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )

    account: Mapped["AccountModel"] = relationship("AccountModel", back_populates="transactions")  # type: ignore

    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"
