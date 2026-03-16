from datetime import date
from decimal import Decimal
from typing import cast
from unittest.mock import AsyncMock

import pytest

from solution.models.account import Account
from solution.models.category import Category, CategoryType
from solution.models.transaction import Transaction
from solution.services.transaction_service import TransactionService


@pytest.mark.asyncio
async def test_get_all_transactions(transaction_service: TransactionService) -> None:
    transactions = [
        Transaction(
            id=1,
            description="Salary",
            amount=Decimal("5000"),
            created_at=date(2026, 3, 1),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=2,
            description="Groceries",
            amount=Decimal("250"),
            created_at=date(2026, 3, 5),
            category_id=2,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=3,
            description="Rent",
            amount=Decimal("1800"),
            created_at=date(2026, 2, 1),
            category_id=3,
            account_id=2,
            is_deleted=False,
        ),
        Transaction(
            id=4,
            description="Deleted transaction",
            amount=Decimal("100"),
            created_at=date(2026, 3, 8),
            category_id=2,
            account_id=1,
            is_deleted=True,
        ),
    ]
    cast(
        AsyncMock,
        transaction_service.transaction_repository.get_all,
    ).return_value = transactions

    result = await transaction_service.get_all_transactions(
        account_id=1,
        month=3,
        year=2026,
    )

    assert len(result) == 2
    assert all(transaction.account_id == 1 for transaction in result)


@pytest.mark.asyncio
async def test_get_all_transactions_month_without_year(
    transaction_service: TransactionService,
) -> None:
    with pytest.raises(ValueError):
        await transaction_service.get_all_transactions(
            account_id=None,
            month=3,
            year=None,
        )


@pytest.mark.asyncio
async def test_add_income_transaction(transaction_service: TransactionService) -> None:
    account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("1000"),
        currency="ILS",
        is_deleted=False,
    )
    category = Category(
        id=1,
        name="Salary",
        category_type=CategoryType.INCOME,
        is_archived=False,
    )
    created_transaction = Transaction(
        id=10,
        description="March salary",
        amount=Decimal("7000"),
        created_at=date.today(),
        category_id=1,
        account_id=1,
        is_deleted=False,
    )

    cast(AsyncMock, transaction_service.account_repository.get).return_value = account
    cast(
        AsyncMock,
        transaction_service.category_repository.get,
    ).return_value = category
    create_mock = cast(AsyncMock, transaction_service.transaction_repository.create)
    create_mock.return_value = created_transaction

    result = await transaction_service.add_income_transaction(
        account_id=1,
        description="March salary",
        amount=Decimal("7000"),
        category_id=1,
    )

    assert result.id == 10
    assert result.description == "March salary"
    assert result.amount == Decimal("7000")
    create_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_expense_transaction(transaction_service: TransactionService) -> None:
    account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("1000"),
        currency="ILS",
        is_deleted=False,
    )
    category = Category(
        id=2,
        name="Groceries",
        category_type=CategoryType.EXPENSE,
        is_archived=False,
    )
    created_transaction = Transaction(
        id=11,
        description="Supermarket",
        amount=Decimal("250"),
        created_at=date.today(),
        category_id=2,
        account_id=1,
        is_deleted=False,
    )

    cast(AsyncMock, transaction_service.account_repository.get).return_value = account
    cast(
        AsyncMock,
        transaction_service.category_repository.get,
    ).return_value = category
    create_mock = cast(AsyncMock, transaction_service.transaction_repository.create)
    create_mock.return_value = created_transaction

    result = await transaction_service.add_expense_transaction(
        account_id=1,
        description="Supermarket",
        amount=Decimal("250"),
        category_id=2,
    )

    assert result.id == 11
    assert result.description == "Supermarket"
    assert result.amount == Decimal("250")
    create_mock.assert_awaited_once()


@pytest.mark.parametrize(
    ("description", "amount"),
    [
        ("", Decimal("100")),
        ("Valid description", Decimal("0")),
        ("Valid description", Decimal("-5")),
    ],
)
@pytest.mark.asyncio
async def test_add_transaction_invalid_basic_data(
    transaction_service: TransactionService,
    description: str,
    amount: Decimal,
) -> None:
    account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("1000"),
        currency="ILS",
        is_deleted=False,
    )
    category = Category(
        id=2,
        name="Groceries",
        category_type=CategoryType.EXPENSE,
        is_archived=False,
    )

    cast(AsyncMock, transaction_service.account_repository.get).return_value = account
    cast(
        AsyncMock,
        transaction_service.category_repository.get,
    ).return_value = category

    with pytest.raises(ValueError):
        await transaction_service.add_expense_transaction(
            account_id=1,
            description=description,
            amount=amount,
            category_id=2,
        )


@pytest.mark.asyncio
async def test_add_transaction_invalid_category_type(
    transaction_service: TransactionService,
) -> None:
    account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("1000"),
        currency="ILS",
        is_deleted=False,
    )
    wrong_category = Category(
        id=1,
        name="Salary",
        category_type=CategoryType.INCOME,
        is_archived=False,
    )

    cast(AsyncMock, transaction_service.account_repository.get).return_value = account
    cast(
        AsyncMock,
        transaction_service.category_repository.get,
    ).return_value = wrong_category

    with pytest.raises(ValueError):
        await transaction_service.add_expense_transaction(
            account_id=1,
            description="Supermarket",
            amount=Decimal("200"),
            category_id=1,
        )


@pytest.mark.asyncio
async def test_delete_transaction(transaction_service: TransactionService) -> None:
    transaction = Transaction(
        id=1,
        description="Groceries",
        amount=Decimal("200"),
        created_at=date(2026, 3, 10),
        category_id=2,
        account_id=1,
        is_deleted=False,
    )
    cast(
        AsyncMock,
        transaction_service.transaction_repository.get,
    ).return_value = transaction

    await transaction_service.delete_transaction(transaction_id=1)

    delete_mock = cast(AsyncMock, transaction_service.transaction_repository.delete)
    delete_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_transaction_already_deleted(
    transaction_service: TransactionService,
) -> None:
    transaction = Transaction(
        id=1,
        description="Groceries",
        amount=Decimal("200"),
        created_at=date(2026, 3, 10),
        category_id=2,
        account_id=1,
        is_deleted=True,
    )
    cast(
        AsyncMock,
        transaction_service.transaction_repository.get,
    ).return_value = transaction

    with pytest.raises(ValueError):
        await transaction_service.delete_transaction(transaction_id=1)
