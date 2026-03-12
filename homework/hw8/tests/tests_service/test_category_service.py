from unittest.mock import Mock
import pytest

from solution.models.models import Category, CategoryType
from solution.services.category_service import CategoryService


@pytest.fixture
def category_repository_mock() -> Mock:
    repository = Mock()
    categories = {
        1: Category(
            id=1, name="Food", category_type=CategoryType.EXPENSE, is_archived=False
        ),
        2: Category(
            id=2, name="Salary", category_type=CategoryType.INCOME, is_archived=False
        ),
    }
    repository.get_all.return_value = list(categories.values())
    repository.get.side_effect = categories.get
    return repository


@pytest.fixture
def transaction_repository_mock() -> Mock:
    repository = Mock()
    repository.get_all.return_value = []
    return repository


@pytest.fixture
def category_service(
    category_repository_mock: Mock,
    transaction_repository_mock: Mock,
) -> CategoryService:
    return CategoryService(
        category_repository=category_repository_mock,
        transaction_repository=transaction_repository_mock,
    )

@pytest.mark.asyncio
async def test_get_all_category(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    result =await category_service.get_all_category()

    assert len(result) == 2
    category_repository_mock.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_add_category(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    new_category = Category(
        id=3,
        name="Transport",
        category_type=CategoryType.EXPENSE,
        is_archived=False,
    )

    category_repository_mock.create.return_value = new_category

    result = await category_service.add_category(
        name="Transport",
        category_type=CategoryType.EXPENSE,
    )

    assert result == new_category
    category_repository_mock.create.assert_called_once()

@pytest.mark.asyncio
async def test_delete_category(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    await category_service.delete_category(1)

    category_repository_mock.get.assert_called_once_with(1)
    category_repository_mock.delete.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_add_category_empty_name(
    category_service: CategoryService,
) -> None:
    with pytest.raises(ValueError, match="Category name cannot be empty"):
       await category_service.add_category(
            name="",
            category_type=CategoryType.EXPENSE,
        )

@pytest.mark.asyncio
async def test_delete_category_with_transaction(
    category_repository_mock: Mock,
) -> None:
    transaction_repository_mock = Mock()

    transaction = Mock()
    transaction.category_id = 1
    transaction.is_deleted = False

    transaction_repository_mock.get_all.return_value = [transaction]

    service = CategoryService(
        category_repository=category_repository_mock,
        transaction_repository=transaction_repository_mock,
    )

    with pytest.raises(
        ValueError,
        match="Cannot delete category that has a transaction",
    ):
        await service.delete_category(1)
