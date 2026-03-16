from solution.repository.base_repository import BaseRepository
from decimal import Decimal
from datetime import date
from solution.models.transaction import Transaction


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self) -> None:
        super().__init__(Transaction)
