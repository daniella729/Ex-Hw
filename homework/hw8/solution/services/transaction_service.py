from datetime import date
from decimal import Decimal
from solution.models.models import Category, CategoryType, Transaction
from solution.repository.account_repository import AccountRepository
from solution.repository.category_repository import CategoryRepository
from solution.repository.transaction_repository import TransactionRepository

FIRST_GENERATED_ID = 1


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        account_repository: AccountRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.account_repository = account_repository

    async def get_all_transactions(
        self, account_id: int | None, month: int | None, year: int | None
    ) -> list[Transaction]:
        transactions = self.transaction_repository.get_all()
        filtered_transactions = []
        for transaction in transactions:
            if transaction.is_deleted:
                continue
            if account_id is not None and transaction.account_id != account_id:
                continue
            if self.match_month_year(transaction, month, year) is False:
                continue
            filtered_transactions.append(transaction)

        return filtered_transactions

    def match_month_year(
        self, transaction: Transaction, month: int | None, year: int | None
    ) -> bool:
        if month is not None and year is None:
            raise ValueError("Month filter requires year")
        if month is not None and transaction.created_at.month != month:
            return False
        if year is not None and transaction.created_at.year != year:
            return False
        else:
            return True

    async def add_income_transaction(
        self,
        account_id:int,
        description: str,
        amount: Decimal,
        category_id:int
    ) -> Transaction:
       return await self.add_transaction(
           description=description,
           amount=amount,
           created_at=date.today(),
           category_id=category_id,
           account_id=account_id,
           expected_category_type=CategoryType.INCOME,
           is_deleted=False
       )
            
            
       
    async def add_expense_transaction(
        self,
        account_id:int,
        description: str,
        amount: Decimal,
        category_id:int
    ) -> Transaction:
       return await self.add_transaction(
           description=description,
           amount=amount,
           created_at=date.today(),
           category_id=category_id,
           account_id=account_id,
           expected_category_type=CategoryType.EXPENSE,
           is_deleted=False
       )

    async def delete_transaction(self, transaction_id: int) -> None:
        transaction = self.transaction_repository.get(transaction_id)
        if transaction is None:
           raise ValueError("Transaction not found")
        if transaction.is_deleted:
            raise ValueError("Transaction already deleted")
        self.transaction_repository.delete(transaction_id)

    async def add_transaction(
        self,
        description: str,
        amount: Decimal,
        created_at: date,
        category_id: int,
        account_id: int,
        expected_category_type: CategoryType,
        is_deleted: bool,
    ) -> Transaction:
        if created_at is None:
            created_at = date.today()
        self.account_repository.get(account_id)
        category = self.category_repository.get(category_id)
        self.validate_transaction_data(
            description=description,
            amount=amount,
            category_type=category.category_type,
            expected_category_type=expected_category_type,
        )
        transaction = Transaction(
            id= self.generate_transaction_id(),
            description=description,
            amount=amount,
            created_at=created_at,
            category_id=category_id,
            account_id=account_id,
            is_deleted=is_deleted,
        )
        return self.transaction_repository.create(transaction)

    def generate_transaction_id(self) -> int:
        transactions = self.transaction_repository.get_all()
        active_transactions = [
            transaction for transaction in transactions if not transaction.is_deleted
        ]
        if active_transactions:
            return max(transaction.id for transaction in transactions) + 1
        else:
            return FIRST_GENERATED_ID

    def validate_transaction_data(
        self,
        description: str,
        amount: Decimal,
        category_type: CategoryType,
        expected_category_type: CategoryType,
    ) -> None:
        if description == "":
            raise ValueError("Description cannot be empty")
        if amount <= Decimal("0"):
            raise ValueError("Amount must be greater than zero")
        if category_type != expected_category_type:
            raise ValueError("Invalid category type for this transaction")
