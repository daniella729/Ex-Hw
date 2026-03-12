from solution.models.models import Transfer
from solution.repository.base_repository import BaseRepository
from solution.repository.csv_accessor import CsvFileAccessor
from decimal import Decimal
from datetime import date

ID = "id"
NAME = "name"
AMOUNT = "amount"
DESCRIPTION = "description"
CREATED_AT = "created_at"


class TransferRepository(BaseRepository[Transfer]):
    def __init__(self, accessor: CsvFileAccessor):
        super().__init__(accessor, Transfer)

    def convert_data(self, row: dict[str, str]) -> Transfer:
        return Transfer(
            id=int(row[ID]),
            description=row[DESCRIPTION],
            amount=Decimal(row[AMOUNT]),
            transfer_date=date.fromisoformat(row["transfer_date"]),
            created_at=date.fromisoformat(row[CREATED_AT]),
            from_account_id=int(row["from_account_id"]),
            to_account_id=int(row["to_account_id"]),
            is_deleted=row["is_deleted"] == "True",
        )

    def data_to_row(self, item: Transfer) -> dict[str, str]:
        return {
            ID: str(item.id),
            DESCRIPTION: item.description,
            AMOUNT: str(item.amount),
            "transfer_date":str(item.transfer_date),
            CREATED_AT: str(item.created_at),
            "from_account_id": str(item.from_account_id),
            "to_account_id": str(item.to_account_id),
            "is_deleted": str(item.is_deleted),
        }
