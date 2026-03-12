from decimal import Decimal

from solution.models.models import Account
from solution.repository.base_repository import BaseRepository
from solution.repository.csv_accessor import CsvFileAccessor

ID = "id"
NAME = "name"


class AccountRepository(BaseRepository[Account]):
    def __init__(self, accessor: CsvFileAccessor):
        super().__init__(accessor, Account)

    def convert_data(self, row: dict[str, str]) -> Account:
        return Account(
            id=int(row[ID]),
            name=row[NAME],
            opening_balance=Decimal(row["opening_balance"]),
            currency=row["currency"],
            is_deleted=row["is_deleted"] == "True",
        )

    def data_to_row(self, item: Account) -> dict[str, str]:
        return {
            ID: str(item.id),
            NAME: item.name,
            "opening_balance": str(item.opening_balance),
            "currency": item.currency,
            "is_deleted": str(item.is_deleted),
        }
