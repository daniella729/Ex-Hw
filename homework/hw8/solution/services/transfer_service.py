from datetime import date
from decimal import Decimal

from solution.models.models import Transfer
from solution.repository.account_repository import AccountRepository
from solution.repository.transfer_repository import TransferRepository

FIRST_GENERATED_ID = 1


class TransferService:
    def __init__(
        self,
        transfer_repository: TransferRepository,
        account_repository: AccountRepository,
    ) -> None:
        self.transfer_repository = transfer_repository
        self.account_repository = account_repository

    async def get_all_transfer(self) -> list[Transfer]:
        transfers = self.transfer_repository.get_all()
        return [transfer for transfer in transfers if not transfer.is_deleted]

    async def add_transfer(
        self,
        description: str,
        amount: Decimal,
        transfer_date:date,
        from_account_id: int,
        to_account_id: int,
    ) -> Transfer:
        from_account=self.account_repository.get(from_account_id)
        if from_account is None:
            raise ValueError("From account not found")
        to_account=self.account_repository.get(to_account_id)
        if to_account is None:
             raise ValueError("To account not found")
        self.validate_transfer_data(
            description=description,
            amount=amount,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
        )
        transafer = Transfer(
            id=self.generate_transfer_id(),
            description=description,
            amount=amount,
            transfer_date=transfer_date,
            created_at=date.today(),
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            is_deleted=False,
        )
        return self.transfer_repository.create(transafer)

    async def delete_transfer(self, transfer_id: int) -> None:
        transfer = self.transfer_repository.get(transfer_id)
        if transfer.is_deleted:
            raise ValueError("Transfer already deleted")

        self.transfer_repository.delete(transfer_id)

    def generate_transfer_id(self) -> int:
        transfers = self.transfer_repository.get_all()
        active_transfers = [
            transfer for transfer in transfers if not transfer.is_deleted
        ]
        if active_transfers:
            return max(transfer.id for transfer in transfers) + 1
        else:
            return FIRST_GENERATED_ID

    def validate_transfer_data(
        self,
        description: str,
        amount: Decimal,
        from_account_id: int,
        to_account_id: int,
    ) -> None:
        if description == "":
            raise ValueError("Description cannot be empty")
        if amount <= Decimal("0"):
            raise ValueError("Amount must be greater than zero")
        if from_account_id == to_account_id:
            raise ValueError("transfer must be between two different accounts")
