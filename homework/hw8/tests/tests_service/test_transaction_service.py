from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from solution.models.models import Category, CategoryType, Transaction
from solution.services.transaction_service import TransactionService


@pytest.fixture
def transaction_repository_mock() -> Mock:
    repository = Mock()
    transaction = {
        1: Transaction(
            id=1,
            description="Salary",
            amount=Decimal("5000"),
            created_at=date(2025, 1, 10),
            category_id=1,
            account_id=1,
        ),
        2: Transaction(
            id=2,
            description="Groceries",
            amount=Decimal("200"),
            created_at=date(2025, 2, 5),
            category_id=2,
            account_id=2,
        ),
        3: Transaction(
            id=3,
            description="Bonus",
            amount=Decimal("1000"),
            created_at=date(2025, 2, 20),
            category_id=1,
            account_id=1,
        ),
    }
    repository.get_all.return_value = list(transaction.values())
    repository.get.side_effect = transaction.get
    return repository


@pytest.fixture
def account_repository_mock() -> Mock:
    repository = Mock()
    repository.get.return_value = Mock()
    return repository


@pytest.fixture
def category_repository_mock() -> Mock:
    repository = Mock()
    repository.get.return_value = Category(
        id=1, name="Salary", category_type=CategoryType.INCOME, is_archived=False
    )
    return repository


@pytest.fixture
def transaction_service(
    transaction_repository_mock: Mock,
    account_repository_mock: Mock,
    category_repository_mock: Mock,
) -> TransactionService:
    return TransactionService(
        transaction_repository=transaction_repository_mock,
        account_repository=account_repository_mock,
        category_repository=category_repository_mock,
    )

@pytest.mark.asyncio
async def test_get_all_transactions_by_account(
    transaction_service: TransactionService,
) -> None:
    result =await  transaction_service.get_all_transactions(
        account_id=1,
        month=None,
        year=None,
    )

    assert len(result) == 2
    assert all(transaction.account_id == 1 for transaction in result)

@pytest.mark.asyncio
async def test_get_all_transactions_by_month_and_year(
    transaction_service: TransactionService,
) -> None:
    result =await  transaction_service.get_all_transactions(
        account_id=None,
        month=2,
        year=2025,
    )

    assert len(result) == 2
    assert all(transaction.created_at.month == 2 for transaction in result)
    assert all(transaction.created_at.year == 2025 for transaction in result)

@pytest.mark.asyncio
async def test_all_transactions_by_account_month_year(
    transaction_service: TransactionService,
) -> None:
    result = await transaction_service.get_all_transactions(
        account_id=1,
        month=2,
        year=2025,
    )

    assert len(result) == 1
    assert result[0].description == "Bonus"

@pytest.mark.asyncio
async def test_all_transactions_month_without_year(
    transaction_service: TransactionService,
) -> None:
    with pytest.raises(ValueError, match="Month filter requires year"):
       await transaction_service.get_all_transactions(
            account_id=None,
            month=2,
            year=None,
        )

@pytest.mark.asyncio
async def test_add_income_transaction(
    transaction_service: TransactionService,
    transaction_repository_mock: Mock,
    account_repository_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    expected_transaction = Transaction(
        id=4,
        description="Freelance",
        amount=Decimal("800"),
        created_at=date.today(),
        category_id=1,
        account_id=1,
        is_deleted=False
    )
    transaction_repository_mock.create.return_value = expected_transaction

    result = await transaction_service.add_income_transaction(
        description="Freelance",
        amount=Decimal("800"),
        category_id=1,
        account_id=1,
    )

    assert result == expected_transaction
    account_repository_mock.get.assert_called_once_with(1)
    category_repository_mock.get.assert_called_once_with(1)
    transaction_repository_mock.create.assert_called_once_with(expected_transaction)

@pytest.mark.asyncio
async def test_add_expense_transaction(
    transaction_repository_mock: Mock,
    account_repository_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get.return_value = Category(
        id=2,
        name="Food",
        category_type=CategoryType.EXPENSE,
    )

    service = TransactionService(
        transaction_repository=transaction_repository_mock,
        account_repository=account_repository_mock,
        category_repository=category_repository_mock,
    )

    expected_transaction = Transaction(
        id=4,
        description="Dinner",
        amount=Decimal("120"),
        created_at=date.today(),
        category_id=2,
        account_id=1,
        is_deleted=False,
    )
    transaction_repository_mock.create.return_value = expected_transaction

    result = await service.add_expense_transaction(
        description="Dinner",
        amount=Decimal("120"),
        category_id=2,
        account_id=1,
        
    )

    assert result == expected_transaction
    transaction_repository_mock.create.assert_called_once_with(expected_transaction)

@pytest.mark.asyncio
async def test_add_transaction_empty_description(
    transaction_service: TransactionService,
) -> None:
    with pytest.raises(ValueError, match="Description cannot be empty"):
        await transaction_service.add_income_transaction(
            description="",
            amount=Decimal("100"),
            category_id=1,
            account_id=1,
        )

@pytest.mark.asyncio
async def test_add_transaction_non_positive_amount(
    transaction_service: TransactionService,
) -> None:
    with pytest.raises(ValueError, match="Amount must be greater than zero"):
       await transaction_service.add_income_transaction(
            description="Salary",
            amount=Decimal("0"),
            category_id=1,
            account_id=1,
            
        )

@pytest.mark.asyncio
async def test_add_transactio_invalid_category_type(
    transaction_repository_mock: Mock,
    account_repository_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get.return_value = Category(
        id=2,
        name="Food",
        category_type=CategoryType.EXPENSE,
    )

    service = TransactionService(
        transaction_repository=transaction_repository_mock,
        account_repository=account_repository_mock,
        category_repository=category_repository_mock,
    )

    with pytest.raises(
        ValueError,
        match="Invalid category type for this transaction",
    ):
        await service.add_income_transaction(
            description="Salary",
            amount=Decimal("1000"),
            category_id=2,
            account_id=1,
           
        )

@pytest.mark.asyncio
async def test_delete_transaction(
    transaction_service: TransactionService,
    transaction_repository_mock: Mock,
) -> None:
    await transaction_service.delete_transaction(2)

    transaction_repository_mock.delete.assert_called_once_with(2)
