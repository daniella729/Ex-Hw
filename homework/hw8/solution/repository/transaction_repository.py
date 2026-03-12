from solution.models.models import Transaction
from solution.repository.base_repository import BaseRepository
from solution.repository.csv_accessor import CsvFileAccessor
from decimal import Decimal
from datetime import date

ID = "id"
NAME = "name"
AMOUNT = "amount"
DESCRIPTION = "description"
CREATED_AT = "created_at"


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self, accessor: CsvFileAccessor):
        super().__init__(accessor, Transaction)

    def convert_data(self, row: dict[str, str]) -> Transaction:
        return Transaction(
            id=int(row[ID]),
            description=row[DESCRIPTION],
            amount=Decimal(row[AMOUNT]),
            created_at=date.fromisoformat(row[CREATED_AT]),
            category_id=int(row["category_id"]),
            account_id=int(row["account_id"]),
            is_deleted=row["is_deleted"] == "True",
        )

    def data_to_row(self, item: Transaction) -> dict[str, str]:
        return {
            ID: str(item.id),
            DESCRIPTION: item.description,
            AMOUNT: str(item.amount),
            CREATED_AT: str(item.created_at),
            "category_id": str(item.category_id),
            "account_id": str(item.account_id),
            "is_deleted": str(item.is_deleted),
        }
