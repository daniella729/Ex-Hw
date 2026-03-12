from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
from datetime import date

SYSTEM_CURRENCY = "ILS"


class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Category:
    id: int
    name: str
    category_type: CategoryType
    is_archived: bool = False


@dataclass
class Transaction:
    id: int
    description: str
    amount: Decimal
    created_at: date
    category_id: int
    account_id: int
    is_deleted: bool = False


@dataclass
class Transfer:
    id: int
    description: str
    amount: Decimal
    transfer_date:date
    created_at: date
    from_account_id: int
    to_account_id: int
    is_deleted: bool = False


@dataclass
class Account:
    id: int
    name: str
    opening_balance: Decimal
    currency: str = SYSTEM_CURRENCY
    is_deleted: bool = False
