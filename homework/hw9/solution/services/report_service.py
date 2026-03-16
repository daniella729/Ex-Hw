from solution.repository.transaction_repository import TransactionRepository
from solution.repository.category_repository import CategoryRepository
from solution.models.category import CategoryType
from decimal import Decimal
from solution.database import async_session_maker
import asyncio
from typing import Optional
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

INVAILD_VALUE = 0


class ReportService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self._session_maker = session_maker or async_session_maker

    async def get_spending_breakdown_by_category(
        self, month: int, year: int
    ) -> list[dict[str, str | Decimal]]:
        async with self._session_maker() as session:
            transactions = await self.transaction_repository.get_all(session)

            categories = await asyncio.gather(
                *[
                    self.category_repository.get(session, transaction.category_id)
                    for transaction in transactions
                ]
            )

            result: dict[str, Decimal] = {}

            for transaction, category in zip(transactions, categories):
                if (
                    transaction.is_deleted
                    or transaction.created_at.month != month
                    or transaction.created_at.year != year
                ):
                    continue

                if category.category_type != CategoryType.EXPENSE:
                    continue

                if category.name not in result:
                    result[category.name] = Decimal(INVAILD_VALUE)

                result[category.name] = result[category.name] + transaction.amount

            return [
                {"category": category_name, "total spending": amount}
                for category_name, amount in result.items()
            ]
