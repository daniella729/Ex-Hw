from typing import NoReturn

from solution.repository.category_repository import CategoryRepository
from solution.repository.account_repository import AccountRepository
from solution.repository.transaction_repository import TransactionRepository
from solution.repository.transfer_repository import TransferRepository


from solution.services.account_service import AccountService
from solution.services.category_service import CategoryService
from solution.services.transaction_service import TransactionService
from solution.services.report_service import ReportService
from solution.services.transfer_service import TransferService
from fastapi import HTTPException, status


def get_account_repository() -> AccountRepository:
    return AccountRepository()


def get_category_repository() -> CategoryRepository:
    return CategoryRepository()


def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository()


def get_transfer_repository() -> TransferRepository:
    return TransferRepository()


def get_account_service() -> AccountService:
    return AccountService(
        account_repository=get_account_repository(),
        transaction_repository=get_transaction_repository(),
        transfer_repository=get_transfer_repository(),
        category_repository=get_category_repository(),
    )


def get_category_service() -> CategoryService:
    return CategoryService(
        category_repository=get_category_repository(),
        transaction_repository=get_transaction_repository(),
    )


def get_transaction_service() -> TransactionService:
    return TransactionService(
        transaction_repository=get_transaction_repository(),
        account_repository=get_account_repository(),
        category_repository=get_category_repository(),
    )


def get_transfer_service() -> TransferService:
    return TransferService(
        transfer_repository=get_transfer_repository(),
        account_repository=get_account_repository(),
    )


def get_report_service() -> ReportService:
    return ReportService(
        transaction_repository=get_transaction_repository(),
        category_repository=get_category_repository(),
    )


def raise_bad_request(detail: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
    )


def raise_not_found(detail: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
    )
