from datetime import date
from decimal import Decimal
from typing import Annotated, Any

from fastapi import APIRouter, Depends

from solution.api.dependencies import (
    get_transaction_service,
    raise_bad_request,
    raise_not_found,
)
from solution.services.transaction_service import TransactionService

NOT_FOUND = "not found"

router = APIRouter(prefix="/transactions", tags=["Transactions"])

TransactionServiceDep = Annotated[
    TransactionService,
    Depends(get_transaction_service),
]


@router.get("", response_model=list)
async def get_all_transactions(
    service: TransactionServiceDep,
    account_id: int | None = None,
    month: int | None = None,
    year: int | None = None,
) -> list:
    try:
        transactions = await service.get_all_transactions(account_id, month, year)
    except ValueError as exception:
        raise_bad_request(str(exception))
    return [
        {
            "id": transaction.id,
            "description": transaction.description,
            "amount": transaction.amount,
            "created_at": transaction.created_at,
            "category_id": transaction.category_id,
            "account_id": transaction.account_id,
            "is_deleted": transaction.is_deleted,
        }
        for transaction in transactions
    ]


@router.post("/income")
async def add_income_transaction(
    account_id: int,
    description: str,
    amount: Decimal,
    category_id: int,
    service: TransactionServiceDep,
) -> dict[str, Any]:
    try:
        transaction = await service.add_income_transaction(
            account_id,
            description,
            amount,
            category_id,
        )

    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message.strip():
            raise_not_found(message)
        raise_bad_request(message)

    return {
        "id": transaction.id,
        "account_id": transaction.account_id,
        "description": transaction.description,
        "amount": transaction.amount,
        "created_at": transaction.created_at,
        "category_id": transaction.category_id,
        "is_deleted": transaction.is_deleted,
    }


@router.post("/expense")
async def add_expense_transaction(
    account_id: int,
    description: str,
    amount: Decimal,
    category_id: int,
    service: TransactionServiceDep,
) -> dict[str, Any]:
    try:
        transaction = await service.add_expense_transaction(
            account_id,
            description,
            amount,
            category_id,
        )

    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message.strip():
            raise_not_found(message)
        raise_bad_request(message)

    return {
        "id": transaction.id,
        "account_id": transaction.account_id,
        "description": transaction.description,
        "amount": transaction.amount,
        "created_at": transaction.created_at,
        "category_id": transaction.category_id,
        "is_deleted": transaction.is_deleted,
    }


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int, service: TransactionServiceDep
) -> None:
    try:
        await service.delete_transaction(transaction_id)
    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message.strip():
            raise_not_found(message)
        raise_bad_request(message)
