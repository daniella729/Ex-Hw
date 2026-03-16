from solution.repository.base_repository import BaseRepository
from decimal import Decimal
from datetime import date
from solution.models.transfer import Transfer


class TransferRepository(BaseRepository[Transfer]):
    def __init__(self) -> None:
        super().__init__(Transfer)
