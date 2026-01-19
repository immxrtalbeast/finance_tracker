from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


@dataclass
class Transaction:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    account_id: UUID = field(default_factory=uuid4)
    category_id: Optional[UUID] = None
    amount: Decimal = Decimal("0.00")
    type: TransactionType = TransactionType.EXPENSE
    description: Optional[str] = None
    date: Optional[datetime] = field(default_factory=datetime.now)
