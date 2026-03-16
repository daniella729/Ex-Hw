from decimal import Decimal
import asyncio
from solution.models.account import Account
from solution.models.category import CategoryType
from solution.models.transaction import Transaction
from solution.repository.account_repository import AccountRepository
from solution.repository.category_repository import CategoryRepository
from solution.repository.transaction_repository import TransactionRepository
from solution.repository.transfer_repository import TransferRepository
from solution.database import async_session_maker
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Optional, Any

FIRST_GENERATED_ID = 1
INITIAL_VALUE = 0


class AccountService:
    def __init__(
        self,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
        transfer_repository: TransferRepository,
        category_repository: CategoryRepository,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.transfer_repository = transfer_repository
        self.category_repository = category_repository
        self._session_maker = session_maker or async_session_maker

    async def get_all_account_with_current_balance(self) -> list:
        async with self._session_maker() as session:
            Accounts = await self.account_repository.get_all(session)
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
        async with self._session_maker() as session:
            async with session.begin():
                account = await self.account_repository.get(session, account_id)
                if account.is_deleted:
                    raise ValueError("Account already deleted")
                if await self.account_has_transaction(account_id):
                    raise ValueError("Cannot delete account that has transaction")
                if await self.account_has_transfer(account_id):
                    raise ValueError("Cannot delete account that has transfer")
                await self.account_repository.delete(session, account_id)

    async def add_account(
        self, name: str, opening_balance: Decimal, currency: str
    ) -> Account:
        self.validate_account_name(name)
        if opening_balance < 0:
            raise ValueError("opening balance cannot be negative")
        account = Account(
            name=name,
            opening_balance=opening_balance,
            currency=currency,
            is_deleted=False,
        )
        async with self._session_maker() as session:
            async with session.begin():
                return await self.account_repository.create(session, account)

    async def net_worth(self) -> Decimal:
        async with self._session_maker() as session:
            accounts = await self.account_repository.get_all(session)
        active_accounts = [account for account in accounts if not account.is_deleted]

        balances = await asyncio.gather(
            *(self.get_account_balance(account.id) for account in active_accounts)
        )
        return sum(balances, start=Decimal(INITIAL_VALUE))

    async def get_account_balance(self, account_id: int) -> Decimal:
        async with self._session_maker() as session:
            account = await self.account_repository.get(session, account_id)
            transactions = await self.transaction_repository.get_all(session)
            transfers = await self.transfer_repository.get_all(session)

            transaction_total = await self.calculate_transaction_total(
                session,
                account_id,
                transactions,
            )
            transfer_total = self.calculate_transfer_total(account_id, transfers)

            return account.opening_balance + transaction_total + transfer_total

    async def calculate_transaction_total(
        self,
        session: Any,
        account_id: int,
        transactions: list[Transaction],
    ) -> Decimal:
        relevant_transactions = [
            transaction
            for transaction in transactions
            if not transaction.is_deleted and transaction.account_id == account_id
        ]

        categories = await asyncio.gather(
            *(
                self.category_repository.get(session, transaction.category_id)
                for transaction in relevant_transactions
            )
        )

        total = Decimal(INITIAL_VALUE)
        for transaction, category in zip(relevant_transactions, categories):
            if category.is_archived:
                continue
            total += self.calculate_transaction_effect(
                transaction,
                category.category_type,
            )
        return total

    def calculate_transfer_total(
        self,
        account_id: int,
        transfers: list,
    ) -> Decimal:
        total = Decimal(INITIAL_VALUE)
        for transfer in transfers:
            if transfer.is_deleted:
                continue
            if transfer.from_account_id == account_id:
                total -= transfer.amount
            elif transfer.to_account_id == account_id:
                total += transfer.amount
        return total

    async def edit_account_name(self, account_id: int, new_name: str) -> Account:
        self.validate_account_name(new_name)
        async with self._session_maker() as session:
            async with session.begin():
                account = await self.account_repository.get(session, account_id)
                if account.is_deleted:
                    raise ValueError("Account is deleted")
                account.name = new_name
                return await self.account_repository.update(session, account)

    def calculate_transaction_effect(
        self, transaction: Transaction, category_type: CategoryType
    ) -> Decimal:
        if category_type == CategoryType.INCOME:
            return transaction.amount
        return -transaction.amount

    def validate_account_name(self, name: str) -> None:
        if name == "":
            raise ValueError("Account name cannot be empty")

    async def account_has_transaction(self, account_id: int) -> bool:
        async with self._session_maker() as session:
            transactions = await self.transaction_repository.get_all(session)
            for transaction in transactions:
                if transaction.is_deleted:
                    continue
                if transaction.account_id == account_id:
                    return True
        return False

    async def account_has_transfer(self, account_id: int) -> bool:
        async with self._session_maker() as session:
            transfers = await self.transfer_repository.get_all(session)
            for transfer in transfers:
                if transfer.is_deleted:
                    continue
                if transfer.from_account_id == account_id:
                    return True
                if transfer.to_account_id == account_id:
                    return True
        return False
