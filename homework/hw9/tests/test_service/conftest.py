from datetime import datetime, date
from decimal import Decimal
from unittest.mock import AsyncMock, Mock
from solution.services.report_service import ReportService
import pytest
from solution.models.transaction import Transaction
from solution.models.transfer import Transfer
from solution.services.transaction_service import TransactionService
from solution.services.transfer_service import TransferService


@pytest.fixture
def report_service() -> ReportService:
    transaction_repo = Mock()
    transaction_repo.get_all = AsyncMock(return_value=[])
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

    return ReportService(
        transaction_repository=transaction_repo,
        category_repository=category_repo,
        session_maker=mock_session_maker,
    )


@pytest.fixture
def transaction_service() -> TransactionService:
    transaction_repo = Mock()
    transaction_repo.get_all = AsyncMock(
        return_value=[
            Transaction(
                id=1,
                description="Salary January",
                amount=Decimal("8500.00"),
                created_at=date(2025, 2, 1),
                category_id=1,
                account_id=1,
                is_deleted=False,
            ),
            Transaction(
                id=2,
                description="Grocery shopping",
                amount=Decimal("320.45"),
                created_at=datetime(2026, 2, 3),
                category_id=2,
                account_id=1,
                is_deleted=False,
            ),
            Transaction(
                id=3,
                description="Electricity bill",
                amount=Decimal("410.70"),
                created_at=datetime(2025, 3, 5),
                category_id=3,
                account_id=2,
                is_deleted=False,
            ),
            Transaction(
                id=4,
                description="Restaurant dinner",
                amount=Decimal("145.90"),
                created_at=datetime(2026, 3, 7),
                category_id=2,
                account_id=1,
                is_deleted=False,
            ),
            Transaction(
                id=5,
                description="Freelance project payment",
                amount=Decimal("1200.00"),
                created_at=datetime(2026, 3, 10),
                category_id=1,
                account_id=3,
                is_deleted=True,
            ),
        ]
    )

    transaction_repo.get = AsyncMock()
    transaction_repo.create = AsyncMock()
    transaction_repo.delete = AsyncMock()

    account_repo = Mock()
    account_repo.get = AsyncMock()

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

    return TransactionService(
        transaction_repository=transaction_repo,
        account_repository=account_repo,
        category_repository=category_repo,
        session_maker=mock_session_maker,
    )


@pytest.fixture
def transfer_service() -> TransferService:
    account_repo = Mock()
    account_repo.get = AsyncMock()
    account_repo.update = AsyncMock()

    transfer_repo = Mock()
    transfer_repo.get_all = AsyncMock(
        return_value=[
            Transfer(
                id=1,
                description="Move money to savings",
                amount=Decimal("250.00"),
                transfer_date=date(2026, 1, 5),
                created_at=datetime(2026, 1, 5, 10, 30),
                from_account_id=1,
                to_account_id=2,
                is_deleted=False,
            ),
            Transfer(
                id=2,
                description="Credit card payment",
                amount=Decimal("1200.50"),
                transfer_date=date(2026, 2, 1),
                created_at=datetime(2026, 2, 1, 18, 45),
                from_account_id=3,
                to_account_id=5,
                is_deleted=False,
            ),
            Transfer(
                id=3,
                description="Internal opening_balance adjustment",
                amount=Decimal("75.25"),
                transfer_date=date(2026, 3, 12),
                created_at=datetime(2026, 3, 12, 9, 15),
                from_account_id=4,
                to_account_id=1,
                is_deleted=False,
            ),
            Transfer(
                id=4,
                description="Move salary to investment account",
                amount=Decimal("3000.00"),
                transfer_date=date(2026, 4, 10),
                created_at=datetime(2026, 4, 10, 14, 0),
                from_account_id=2,
                to_account_id=6,
                is_deleted=False,
            ),
            Transfer(
                id=5,
                description="Incorrect transfer reverted",
                amount=Decimal("150.00"),
                transfer_date=date(2026, 5, 20),
                created_at=datetime(2026, 5, 20, 12, 20),
                from_account_id=7,
                to_account_id=8,
                is_deleted=True,
            ),
        ]
    )
    transfer_repo.get = AsyncMock()
    transfer_repo.delete = AsyncMock()
    transfer_repo.create = AsyncMock()

    mock_session = Mock()
    begin_context = AsyncMock()
    begin_context.__aenter__.return_value = None
    begin_context.__aexit__.return_value = None
    mock_session.begin.return_value = begin_context

    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_session
    mock_context_manager.__aexit__.return_value = None

    mock_session_maker = Mock(return_value=mock_context_manager)

    return TransferService(
        transfer_repository=transfer_repo,
        account_repository=account_repo,
        session_maker=mock_session_maker,
    )
