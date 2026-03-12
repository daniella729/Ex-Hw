from decimal import Decimal
from unittest.mock import Mock
from datetime import date
import pytest

from solution.models.models import (
    Account,
    Category,
    CategoryType,
    Transaction,
    Transfer,
)
from solution.services.account_service import AccountService


@pytest.fixture
def account_repository_mock() -> Mock:
    repository = Mock()
    accounts = {
        1: Account(
            id=1,
            name="Main",
            opening_balance=Decimal("1500"),
            currency="ILS",
            is_deleted=False,
        ),
        2: Account(
            id=2,
            name="Credit Card",
            opening_balance=Decimal("1000"),
            currency="ILS",
            is_deleted=False,
        ),
    }
    repository.get_all.return_value = list(accounts.values())
    repository.get.side_effect = accounts.get
    return repository


@pytest.fixture
def transaction_repository_mock() -> Mock:
    repository = Mock()
    repository.get_all.return_value = [
        Transaction(
            id=1,
            description="Coffee",
            amount=Decimal("10"),
            created_at=date(2025, 1, 1),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=2,
            description="Groceries",
            amount=Decimal("50"),
            created_at=date(2025, 1, 2),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
    ]
    return repository


@pytest.fixture
def transfer_repository_mock() -> Mock:
    repository = Mock()
    repository.get_all.return_value = [
        Transfer(
            id=1,
            description="Move money",
            amount=Decimal("200"),
            transfer_date=date(2025,1,2),
            created_at=date(2025, 1, 1),
            from_account_id=1,
            to_account_id=2,
            is_deleted=False,
        ),
        Transfer(
            id=2,
            description="Pay credit",
            amount=Decimal("300"),
             transfer_date=date(2025,1,2),
            created_at=date(2025, 1, 2),
            from_account_id=1,
            to_account_id=2,
            is_deleted=False,
        ),
    ]
    return repository


@pytest.fixture
def category_repository_mock() -> Mock:
    repository = Mock()
    categories = {
        1: Category(
            id=1,
            name="Salary",
            category_type=CategoryType.INCOME,
            is_archived=False,
        ),
        2: Category(
            id=2,
            name="Food",
            category_type=CategoryType.EXPENSE,
            is_archived=False,
        ),
    }
    repository.get.side_effect = categories.get
    repository.get_all.return_value = list(categories.values())
    return repository


@pytest.fixture
def account_service(
    account_repository_mock: Mock,
    transaction_repository_mock: Mock,
    transfer_repository_mock: Mock,
    category_repository_mock: Mock,
) -> AccountService:
    return AccountService(
        account_repository=account_repository_mock,
        transaction_repository=transaction_repository_mock,
        transfer_repository=transfer_repository_mock,
        category_repository=category_repository_mock,
    )

@pytest.mark.asyncio
async def test_get_all_account_with_current_balance(
    account_service: AccountService,
) -> None:
    result = await account_service.get_all_account_with_current_balance()

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["name"] == "Main"
    assert result[0]["opening_balance"] == Decimal("1500")
    assert result[0]["current_balance"] == Decimal("1060")
    assert result[0]["currency"] == "ILS"
    assert result[0]["is_deleted"] is False

@pytest.mark.asyncio
async def test_add_account(
    account_service: AccountService,
    account_repository_mock: Mock,
) -> None:
    new_account = Account(
        id=3,
        name="Cash",
        opening_balance=Decimal("300"),
    )
    account_repository_mock.create.return_value = new_account

    result =  await account_service.add_account(
        name="Cash",
        opening_balance=Decimal("300"),
        currency="ILS",
    )

    assert result == new_account
    account_repository_mock.create.assert_called_once()

@pytest.mark.asyncio
async def test_add_account_empty_name(
    account_service: AccountService,
) -> None:
    with pytest.raises(ValueError, match="Account name cannot be empty"):
         await account_service.add_account(
            name="", opening_balance=Decimal("100"), currency="ILS"
        )

@pytest.mark.asyncio
async def test_delete_account(
    category_repository_mock: Mock,
) -> None:
    account_repository_mock = Mock()
    account_repository_mock.get.return_value = Account(
        id=3,
        name="Cash",
        opening_balance=Decimal("100"),
        currency="ILS",
        is_deleted=False
    )

    transaction_repository_mock = Mock()
    transaction_repository_mock.get_all.return_value = []

    transfer_repository_mock = Mock()
    transfer_repository_mock.get_all.return_value = []

    service = AccountService(
        account_repository=account_repository_mock,
        transaction_repository=transaction_repository_mock,
        transfer_repository=transfer_repository_mock,
        category_repository=category_repository_mock,
    )

    await service.delete_account(3)

    account_repository_mock.delete.assert_called_once_with(3)

@pytest.mark.asyncio
async def test_delete_account_with_transaction(
    account_repository_mock: Mock,
    transfer_repository_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    transaction_repository_mock = Mock()
    transaction_repository_mock.get_all.return_value = [
        Transaction(
            id=1,
            description="Salary",
            amount=Decimal("100"),
            created_at=date(2025, 1, 1),
            category_id=1,
            account_id=1,
            is_deleted=False,
        )
    ]

    service = AccountService(
        account_repository=account_repository_mock,
        transaction_repository=transaction_repository_mock,
        transfer_repository=transfer_repository_mock,
        category_repository=category_repository_mock,
    )

    with pytest.raises(
        ValueError,
        match="Cannot delete account that has transaction",
    ):
        await service.delete_account(1)

@pytest.mark.asyncio
async def test_get_account_balance(
    account_service: AccountService,
) -> None:
    result =  await account_service.get_account_balance(1)

    assert result == Decimal("1060")

@pytest.mark.asyncio
async def test_edit_account_name(
    account_service: AccountService,
    account_repository_mock: Mock,
) -> None:
    updated_account = Account(
        id=1,
        name="Main Updated",
        opening_balance=Decimal("1500"),
        currency="ILS",
        is_deleted=False,
    )
    account_repository_mock.update.return_value = updated_account
    account_repository_mock.get.return_value = updated_account

    result = await account_service.edit_account_name(
        account_id=1,
        new_name="Main Updated",
    )

    assert result == updated_account
    account_repository_mock.update.assert_called_once()

@pytest.mark.asyncio
async def test_edit_account_name_empty(
    account_service: AccountService,
) -> None:
    with pytest.raises(ValueError, match="Account name cannot be empty"):
        await account_service.edit_account_name(
            account_id=1,
            new_name="",
        )

@pytest.mark.asyncio
async def test_calculate_transaction_effect_income(
    account_service: AccountService,
) -> None:
    transaction = Transaction(
        id=1,
        description="Salary",
        amount=Decimal("500"),
        created_at=date(2025, 1, 1),
        category_id=1,
        account_id=1,
        is_deleted=False,
    )

    result =   account_service.calculate_transaction_effect(transaction)

    assert result == Decimal("500")

@pytest.mark.asyncio
async def test_calculate_transaction_effect_expense(
    account_service: AccountService,
) -> None:
    transaction = Transaction(
        id=2,
        description="Food",
        amount=Decimal("200"),
        created_at=date(2025, 1, 2),
        category_id=2,
        account_id=1,
        is_deleted=False,
    )

    result =  account_service.calculate_transaction_effect(transaction)

    assert result == Decimal("-200")
