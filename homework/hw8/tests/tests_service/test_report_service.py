import pytest
from unittest.mock import Mock
from solution.services.report_service import ReportService
from solution.models.models import Transaction, Category, CategoryType
from decimal import Decimal
import datetime


@pytest.fixture
def transaction_mock() -> Mock:
    mock = Mock()
    mock.get_all.return_value = [
        Transaction(
            1, "Salary", Decimal("5000"), datetime.datetime(2026, 3, 1), 2, 1, False
        ),
        Transaction(
            2,
            "Groceries",
            Decimal("200"),
            datetime.datetime(2026, 3, 2),
            1,
            1,
            False,
        ),
        Transaction(
            3,
            "Freelance",
            Decimal("1500"),
            datetime.datetime(2026, 2, 25),
            3,
            3,
            False,
        ),
        Transaction(
            4, "Milk", Decimal("800"), datetime.datetime(2026, 3, 3), 1, 1, False
        ),
        Transaction(
            5,
            "Electricity",
            Decimal("100"),
            datetime.datetime(2026, 3, 4),
            1,
            1,
            True,
        ),
    ]
    return mock


def get_category(key: str) -> Category:

    if int(key) == 1:
        return Category(
            id=1,
            name="Groceries",
            category_type=CategoryType.EXPENSE,
            is_archived=False,
        )
    elif int(key) == 2:
        return Category(
            id=2, name="Salary", category_type=CategoryType.INCOME, is_archived=False
        )
    elif int(key) == 3:
        return Category(
            id=3,
            name="Freelance",
            category_type=CategoryType.EXPENSE,
            is_archived=False,
        )
    else:
        raise ValueError(f"Unknown category id: {key}")


@pytest.fixture
def category_mock() -> Mock:
    mock = Mock()
    mock.get.side_effect = get_category
    return mock


@pytest.fixture
def report_service(transaction_mock: Mock, category_mock: Mock) -> ReportService:
    return ReportService(transaction_mock, category_mock)

@pytest.mark.asyncio
async def test_get_spending_breakdown(report_service: ReportService) -> None:
    expected = [
        {"category": "Freelance", "total spending": Decimal("1500")},
    ]
    result = await report_service.get_spending_breakdown_by_category(month=2, year=2026)
    assert result == expected

@pytest.mark.asyncio
async def test_get_spending_breakdown_no_expenses(report_service: ReportService) -> None:
    result =await report_service.get_spending_breakdown_by_category(month=1, year=2026)
    assert len(result) == 0

@pytest.mark.asyncio
async def test_get_spending_breakdown_multiple_expenses(
    report_service: ReportService,
) -> None:

    expected = [
        {"category": "Groceries", "total spending": Decimal("1000")},  # 200 + 800
    ]
    result = await report_service.get_spending_breakdown_by_category(month=3, year=2026)
    assert result == expected
