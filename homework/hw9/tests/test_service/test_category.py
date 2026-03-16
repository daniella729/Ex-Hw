from typing import cast
from unittest.mock import AsyncMock

import pytest

from solution.models.category import Category, CategoryType
from solution.models.transaction import Transaction
from solution.services.category_service import CategoryService


@pytest.mark.asyncio
async def test_get_all_category(category_service: CategoryService) -> None:
    result = await category_service.get_all_category()

    assert len(result) == 5
    assert all(not category.is_archived for category in result)


@pytest.mark.asyncio
async def test_add_category_with_empty_name(
    category_service: CategoryService,
) -> None:
    with pytest.raises(ValueError):
        await category_service.add_category("", CategoryType.INCOME)


@pytest.mark.asyncio
async def test_add_category(category_service: CategoryService) -> None:
    created_category = Category(
        id=7,
        name="Bonus",
        category_type=CategoryType.INCOME,
        is_archived=False,
    )
    create_mock = cast(AsyncMock, category_service.category_repository.create)
    create_mock.return_value = created_category

    result = await category_service.add_category("Bonus", CategoryType.INCOME)

    assert result.id == 7
    assert result.name == "Bonus"
    assert result.category_type == CategoryType.INCOME
    create_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_category(category_service: CategoryService) -> None:
    category = Category(
        id=5,
        name="Utilities",
        category_type=CategoryType.EXPENSE,
        is_archived=False,
    )

    cast(AsyncMock, category_service.category_repository.get).return_value = category
    cast(
        AsyncMock,
        category_service.transaction_repository.get_all,
    ).return_value = []

    await category_service.delete_category(category_id=5)

    delete_mock = cast(AsyncMock, category_service.category_repository.delete)
    delete_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_archived_category(category_service: CategoryService) -> None:
    archived_category = Category(
        id=4,
        name="Groceries",
        category_type=CategoryType.EXPENSE,
        is_archived=True,
    )
    cast(
        AsyncMock,
        category_service.category_repository.get,
    ).return_value = archived_category

    with pytest.raises(ValueError):
        await category_service.delete_category(category_id=4)


@pytest.mark.asyncio
async def test_delete_category_with_transaction(
    category_service: CategoryService,
) -> None:
    category = Category(
        id=3,
        name="Rent",
        category_type=CategoryType.EXPENSE,
        is_archived=False,
    )
    transaction = Transaction(
        id=1,
        description="Monthly rent",
        amount=1000,
        created_at=None,
        category_id=3,
        account_id=1,
        is_deleted=False,
    )

    cast(AsyncMock, category_service.category_repository.get).return_value = category
    cast(
        AsyncMock,
        category_service.transaction_repository.get_all,
    ).return_value = [transaction]

    with pytest.raises(ValueError):
        await category_service.delete_category(category_id=3)


@pytest.mark.asyncio
async def test_category_has_transaction_returns_true(
    category_service: CategoryService,
) -> None:
    transaction = Transaction(
        id=1,
        description="Electricity bill",
        amount=300,
        created_at=None,
        category_id=5,
        account_id=1,
        is_deleted=False,
    )
    cast(
        AsyncMock,
        category_service.transaction_repository.get_all,
    ).return_value = [transaction]

    result = await category_service.category_has_transaction(category_id=5)

    assert result is True


@pytest.mark.asyncio
async def test_category_has_transaction_returns_false(
    category_service: CategoryService,
) -> None:
    transaction = Transaction(
        id=1,
        description="Old deleted transaction",
        amount=300,
        created_at=None,
        category_id=5,
        account_id=1,
        is_deleted=True,
    )
    cast(
        AsyncMock,
        category_service.transaction_repository.get_all,
    ).return_value = [transaction]

    result = await category_service.category_has_transaction(category_id=5)

    assert result is False
