from decimal import Decimal

from solution.repository.base_repository import BaseRepository
from solution.models.account import Account


class AccountRepository(BaseRepository[Account]):
    def __init__(self) -> None:
        super().__init__(Account)
