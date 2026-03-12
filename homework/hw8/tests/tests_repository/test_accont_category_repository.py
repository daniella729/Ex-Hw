from unittest.mock import Mock
from decimal import Decimal
import pytest

from solution.repository.account_repository import AccountRepository
from solution.repository.category_repository import CategoryRepository
from solution.models.models import Account, Category, CategoryType


@pytest.fixture
def account_accessor_mock() -> Mock:
    accessor = Mock()
    accessor.read.return_value = [
        {
            "id": "1",
            "name": "Main",
            "opening_balance": "1500",
            "currency": "ILS",
            "is_deleted": "False",
        },
        {
            "id": "2",
            "name": "Credit Card",
            "opening_balance": "1000",
            "currency": "ILS",
            "is_deleted": "False",
        },
    ]
    return accessor


@pytest.fixture
def account_repository(account_accessor_mock: Mock) -> AccountRepository:
    return AccountRepository(account_accessor_mock)


@pytest.fixture
def category_accessor_mock() -> Mock:
    accessor = Mock()
    accessor.read.return_value = [
        {"id": "1", "name": "Food", "category_type": "expense", "is_archived": "False"},
        {
            "id": "2",
            "name": "Salary",
            "category_type": "income",
            "is_archived": "False",
        },
    ]
    return accessor


@pytest.fixture
def category_repository(category_accessor_mock: Mock) -> CategoryRepository:
    return CategoryRepository(category_accessor_mock)


def test_account_get_all(
    account_repository: AccountRepository, account_accessor_mock: Mock
) -> None:
    result = account_repository.get_all()

    expected = [
        Account(
            id=1,
            name="Main",
            opening_balance=Decimal("1500"),
            currency="ILS",
            is_deleted=False,
        ),
        Account(
            id=2,
            name="Credit Card",
            opening_balance=Decimal("1000"),
            currency="ILS",
            is_deleted=False,
        ),
    ]
    assert result == expected
    account_accessor_mock.read.assert_called_once_with()


def test_account_create(
    account_repository: AccountRepository, account_accessor_mock: Mock
) -> None:
    new_account = Account(
        id=3,
        name="Savings",
        opening_balance=Decimal("500"),
        currency="ILS",
        is_deleted=False,
    )

    account_repository.create(new_account)

    account_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "name": "Main",
                "opening_balance": "1500",
                "currency": "ILS",
                "is_deleted": "False",
            },
            {
                "id": "2",
                "name": "Credit Card",
                "opening_balance": "1000",
                "currency": "ILS",
                "is_deleted": "False",
            },
            {
                "id": "3",
                "name": "Savings",
                "opening_balance": "500",
                "currency": "ILS",
                "is_deleted": "False",
            },
        ]
    )


def test_account_update(
    account_repository: AccountRepository, account_accessor_mock: Mock
) -> None:
    updated_account = Account(
        id=1,
        name="Main Updated",
        opening_balance=Decimal("1600"),
        currency="ILS",
        is_deleted=False,
    )

    account_repository.update(updated_account)

    account_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "name": "Main Updated",
                "opening_balance": "1600",
                "currency": "ILS",
                "is_deleted": "False",
            },
            {
                "id": "2",
                "name": "Credit Card",
                "opening_balance": "1000",
                "currency": "ILS",
                "is_deleted": "False",
            },
        ]
    )


def test_account_get(account_repository: AccountRepository) -> None:
    account = account_repository.get(1)
    excepted = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("1500"),
        currency="ILS",
        is_deleted=False,
    )
    assert account == excepted


def test_account_delete(
    account_repository: AccountRepository, account_accessor_mock: Mock
) -> None:
    account_repository.delete(1)
    account_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "name": "Main",
                "opening_balance": "1500",
                "currency": "ILS",
                "is_deleted": "True",
            },
            {
                "id": "2",
                "name": "Credit Card",
                "opening_balance": "1000",
                "currency": "ILS",
                "is_deleted": "False",
            },
        ]
    )
    ##


def test_category_get_all(
    category_repository: CategoryRepository, category_accessor_mock: Mock
) -> None:
    result = category_repository.get_all()

    expected = [
        Category(
            id=1, name="Food", category_type=CategoryType("expense"), is_archived=False
        ),
        Category(
            id=2, name="Salary", category_type=CategoryType("income"), is_archived=False
        ),
    ]
    assert result == expected
    category_accessor_mock.read.assert_called_once_with()


def test_category_create(
    category_repository: CategoryRepository, category_accessor_mock: Mock
) -> None:
    new_category = Category(
        id=3, name="Savings", category_type=CategoryType("income"), is_archived=False
    )

    category_repository.create(new_category)

    category_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "name": "Food",
                "category_type": "expense",
                "is_archived": "False",
            },
            {
                "id": "2",
                "name": "Salary",
                "category_type": "income",
                "is_archived": "False",
            },
            {
                "id": "3",
                "name": "Savings",
                "category_type": "income",
                "is_archived": "False",
            },
        ]
    )


def test_category_update(
    category_repository: CategoryRepository, category_accessor_mock: Mock
) -> None:
    updated_category = Category(
        id=1, name="Game", category_type=CategoryType("expense"), is_archived=False
    )

    category_repository.update(updated_category)

    category_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "name": "Game",
                "category_type": "expense",
                "is_archived": "False",
            },
            {
                "id": "2",
                "name": "Salary",
                "category_type": "income",
                "is_archived": "False",
            },
        ]
    )


def test_category_get(category_repository: CategoryRepository) -> None:
    category = category_repository.get(1)
    excepted = Category(
        id=1, name="Food", category_type=CategoryType("expense"), is_archived=False
    )
    assert category == excepted


def test_category_delete(
    category_repository: CategoryRepository, category_accessor_mock: Mock
) -> None:
    category_repository.delete(1)
    category_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "name": "Food",
                "category_type": "expense",
                "is_archived": "True",
            },
            {
                "id": "2",
                "name": "Salary",
                "category_type": "income",
                "is_archived": "False",
            },
        ]
    )
