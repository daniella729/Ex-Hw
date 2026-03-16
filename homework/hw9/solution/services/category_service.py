from solution.models.category import Category, CategoryType
from solution.repository.category_repository import CategoryRepository
from solution.repository.transaction_repository import TransactionRepository
from solution.database import async_session_maker
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Optional

FIRST_GENERATED_ID = 1


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        transaction_repository: TransactionRepository,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self.category_repository = category_repository
        self.transaction_repository = transaction_repository
        self._session_maker = session_maker or async_session_maker

    async def add_category(self, name: str, category_type: CategoryType) -> Category:
        self.validate_category_name(name)
        category = Category(
            name=name,
            category_type=category_type,
        )
        async with self._session_maker() as session:
            async with session.begin():
                return await self.category_repository.create(session, category)

    async def delete_category(self, category_id: int) -> None:
        async with self._session_maker() as session:
            async with session.begin():
                category = await self.category_repository.get(session, category_id)
                if category.is_archived:
                    raise ValueError("Category already archived")
                if await self.category_has_transaction(category_id):
                    raise ValueError("Cannot delete category that has a transaction")
                await self.category_repository.delete(session, category_id)

    async def get_all_category(self) -> list[Category]:
        async with self._session_maker() as session:
            categories = await self.category_repository.get_all(session)
        return [category for category in categories if not category.is_archived]

    def validate_category_name(self, name: str) -> None:
        if name == "":
            raise ValueError("Category name cannot be empty")

    async def category_has_transaction(self, category_id: int) -> bool:
        async with self._session_maker() as session:
            transactions = await self.transaction_repository.get_all(session)
        for transaction in transactions:
            if transaction.is_deleted:
                continue
            if transaction.category_id == category_id:
                return True
        return False
