from decimal import Decimal
from unittest.mock import AsyncMock, Mock
import pytest
from solution.models.account import Account
from solution.services.account_service import AccountService
from solution.models.category import Category
from solution.models.category import CategoryType
from solution.services.category_service import CategoryService


@pytest.fixture
def account_service() -> AccountService:
    account_repo = Mock()
    account_repo.get_all = AsyncMock(
        return_value=[
            Account(
                id=1,
                name="Main",
                opening_balance=Decimal("5000"),
                currency="ILS",
                is_deleted=False,
            ),
            Account(
                id=2,
                name="Savings",
                opening_balance=Decimal("2000"),
                currency="ILS",
                is_deleted=True,
            ),
            Account(
                id=3,
                name="Home",
                opening_balance=Decimal("1500"),
                currency="ILS",
                is_deleted=False,
            ),
            Account(
                id=4,
                name="Car",
                opening_balance=Decimal("0"),
                currency="ILS",
                is_deleted=False,
            ),
            Account(
                id=5,
                name="Trip",
                opening_balance=Decimal("1234"),
                currency="ILS",
                is_deleted=False,
            ),
            Account(
                id=6,
                name="Weekend",
                opening_balance=Decimal("0"),
                currency="ILS",
                is_deleted=True,
            ),
        ]
    )
    account_repo.get = AsyncMock()
    account_repo.update = AsyncMock()
    account_repo.create = AsyncMock()
    account_repo.delete = AsyncMock()
    transaction_repo = Mock()
    transaction_repo.get_all = AsyncMock(return_value=[])
    transfer_repo = Mock()
    transfer_repo.get_all = AsyncMock(return_value=[])
    category_repo = Mock()
    category_repo.get = AsyncMock()

    mock_session = Mock()
    begin_context = AsyncMock()
    begin_context.__aenter__.return_value = None
    begin_context.__aexit__.return_value = None
    mock_session.begin.return_value = begin_context

    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_session
    mock_context_manager.__aexit__.return_value = None

    mock_session_maker = Mock(return_value=mock_context_manager)

    return AccountService(
        account_repository=account_repo,
        transaction_repository=transaction_repo,
        transfer_repository=transfer_repo,
        category_repository=category_repo,
        session_maker=mock_session_maker,
    )


@pytest.fixture
def category_service() -> CategoryService:

    category_repo = Mock()
    category_repo.get_all = AsyncMock(
        return_value=[
            Category(
                id=1,
                name="Salary",
                category_type=CategoryType.INCOME,
                is_archived=False,
            ),
            Category(
                id=2,
                name="Freelance",
                category_type=CategoryType.INCOME,
                is_archived=False,
            ),
            Category(
                id=3, name="Rent", category_type=CategoryType.EXPENSE, is_archived=False
            ),
            Category(
                id=4,
                name="Groceries",
                category_type=CategoryType.EXPENSE,
                is_archived=True,
            ),
            Category(
                id=5,
                name="Utilities",
                category_type=CategoryType.EXPENSE,
                is_archived=False,
            ),
            Category(
                id=6,
                name="Entertainment",
                category_type=CategoryType.EXPENSE,
                is_archived=False,
            ),
        ]
    )
    category_repo.get = AsyncMock()
    category_repo.create = AsyncMock()
    category_repo.delete = AsyncMock()
    transaction_repo = Mock()
    transaction_repo.get_all = AsyncMock(return_value=[])

    mock_session = Mock()
    begin_context = AsyncMock()
    begin_context.__aenter__.return_value = None
    begin_context.__aexit__.return_value = None
    mock_session.begin.return_value = begin_context

    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_session
    mock_context_manager.__aexit__.return_value = None

    mock_session_maker = Mock(return_value=mock_context_manager)

    return CategoryService(
        category_repository=category_repo,
        transaction_repository=transaction_repo,
        session_maker=mock_session_maker,
    )
