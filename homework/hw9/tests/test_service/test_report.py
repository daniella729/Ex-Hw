from datetime import date
from decimal import Decimal
from typing import cast
from unittest.mock import AsyncMock

import pytest

from solution.models.category import Category, CategoryType
from solution.models.transaction import Transaction
from solution.services.report_service import ReportService


@pytest.mark.asyncio
async def test_get_spending_breakdown_by_category(
    report_service: ReportService,
) -> None:
    transactions = [
        Transaction(
            id=1,
            description="Supermarket",
            amount=Decimal("200"),
            created_at=date(2026, 3, 10),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=2,
            description="Electricity",
            amount=Decimal("150"),
            created_at=date(2026, 3, 12),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=3,
            description="Salary",
            amount=Decimal("9000"),
            created_at=date(2026, 3, 1),
            category_id=2,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=4,
            description="Old grocery",
            amount=Decimal("80"),
            created_at=date(2026, 2, 25),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=5,
            description="Deleted expense",
            amount=Decimal("50"),
            created_at=date(2026, 3, 20),
            category_id=1,
            account_id=1,
            is_deleted=True,
        ),
    ]

    expense_category = Category(
        id=1,
        name="Bills",
        category_type=CategoryType.EXPENSE,
        is_archived=False,
    )
    income_category = Category(
        id=2,
        name="Salary",
        category_type=CategoryType.INCOME,
        is_archived=False,
    )

    cast(
        AsyncMock,
        report_service.transaction_repository.get_all,
    ).return_value = transactions

    cast(AsyncMock, report_service.category_repository.get).side_effect = [
        expense_category,
        expense_category,
        income_category,
        expense_category,
        expense_category,
    ]

    result = await report_service.get_spending_breakdown_by_category(
        month=3,
        year=2026,
    )

    assert result == [
        {
            "category": "Bills",
            "total spending": Decimal("350"),
        }
    ]
