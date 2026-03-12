from decimal import Decimal
import asyncio
from solution.models.models import Account, CategoryType, Transaction
from solution.repository.account_repository import AccountRepository
from solution.repository.category_repository import CategoryRepository
from solution.repository.transaction_repository import TransactionRepository
from solution.repository.transfer_repository import TransferRepository

FIRST_GENERATED_ID = 1
INITIAL_VALUE = 0


class AccountService:
    def __init__(
        self,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
        transfer_repository: TransferRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.transfer_repository = transfer_repository
        self.category_repository = category_repository

    async def get_all_account_with_current_balance(self) -> list:
        Accounts = self.account_repository.get_all()
        active_accounts = [account for account in Accounts if not account.is_deleted]

        balances = await asyncio.gather(
            *(self.get_account_balance(account.id) for account in active_accounts)
        )
        result = []
        for account, balance in zip(active_accounts, balances):
            result.append(
                {
                    "id": account.id,
                    "name": account.name,
                    "opening_balance": account.opening_balance,
                    "current_balance": balance,
                    "currency": account.currency,
                    "is_deleted": account.is_deleted,
                }
            )
        return result

    async def delete_account(self, account_id: int) -> None:
        account = self.account_repository.get(account_id)
        if account.is_deleted:
            raise ValueError("Account already deleted")
        if self.account_has_transaction(account_id):
            raise ValueError("Cannot delete account that has transaction")
        if self.account_has_transfer(account_id):
            raise ValueError("Cannot delete account that has transfer")
        self.account_repository.delete(account_id)

    async def add_account(
        self, name: str, opening_balance: Decimal, currency: str
    ) -> Account:
        self.validate_account_name(name)
        if opening_balance < 0:
            raise ValueError("opening balance cannot be negative")
        account = Account(
            id=self.generate_account_id(),
            name=name,
            opening_balance=opening_balance,
            currency=currency,
            is_deleted=False,
        )
        return self.account_repository.create(account)

    async def net_worth(self) -> Decimal:
        accounts = self.account_repository.get_all()
        net_worth = Decimal(INITIAL_VALUE)
        active_accounts = [account for account in accounts if not account.is_deleted]

        balances = await asyncio.gather(
            *(self.get_account_balance(account.id) for account in active_accounts)
        )
        return sum(balances, start=Decimal(INITIAL_VALUE))

    async def get_account_balance(self, account_id: int) -> Decimal:
        account = self.account_repository.get(account_id)

        transaction_total = sum(
            self.calculate_transaction_effect(transaction)
            for transaction in self.transaction_repository.get_all()
            if not transaction.is_deleted
            and transaction.account_id == account_id
            and not self.category_repository.get(transaction.category_id).is_archived
        )

        transfer_total = sum(
            (
                -transfer.amount
                if transfer.from_account_id == account_id
                else transfer.amount
            )
            for transfer in self.transfer_repository.get_all()
            if not transfer.is_deleted
            and (
                transfer.from_account_id == account_id
                or transfer.to_account_id == account_id
            )
        )

        return account.opening_balance + transaction_total + transfer_total

    async def edit_account_name(self, account_id: int, new_name: str) -> Account:
        self.validate_account_name(new_name)
        account = self.account_repository.get(account_id)
        if account.is_deleted:
            raise ValueError("Account is deleted")
        update_account = Account(
            id=account.id,
            name=new_name,
            opening_balance=account.opening_balance,
            currency=account.currency,
            is_deleted=account.is_deleted,
        )
        return self.account_repository.update(update_account)

    def calculate_transaction_effect(self, transaction: Transaction) -> Decimal:
        category = self.category_repository.get(transaction.category_id)
        if category.category_type == CategoryType.INCOME:
            return transaction.amount
        return -transaction.amount

    def generate_account_id(self) -> int:
        accounts = self.account_repository.get_all()
        active_accounts = [account for account in accounts if not account.is_deleted]
        if active_accounts:
            return max(account.id for account in accounts) + 1
        else:
            return FIRST_GENERATED_ID

    def validate_account_name(self, name: str) -> None:
        if name == "":
            raise ValueError("Account name cannot be empty")

    def account_has_transaction(self, account_id: int) -> bool:
        transactions = self.transaction_repository.get_all()
        for transaction in transactions:
            if transaction.is_deleted:
                continue
            if transaction.account_id == account_id:
                return True
        return False

    def account_has_transfer(self, account_id: int) -> bool:
        transfers = self.transfer_repository.get_all()
        for transfer in transfers:
            if transfer.is_deleted:
                continue
            if transfer.from_account_id == account_id:
                return True
            if transfer.to_account_id == account_id:
                return True
        return False
