from decimal import Decimal
from typing import Annotated, Any
from fastapi import APIRouter, Body, Depends, HTTPException, status

from solution.api.dependencies import (
    get_account_service,
    raise_bad_request,
    raise_not_found,
)
from solution.services.account_service import AccountService

NOT_FOUND = "not found"
router = APIRouter(prefix="/accounts", tags=["Accounts"])
AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]


@router.get("", response_model=list)
async def get_all_accounts(service: AccountServiceDep) -> list:
    try:
        return await service.get_all_account_with_current_balance()
    except ValueError as exception:
        raise_bad_request(str(exception))


@router.post("")
async def add_account(
    name: str, opening_balance: Decimal, currency_just_ILS: str, service: AccountServiceDep
) -> dict[str, Any]:
    try:
        account = await service.add_account(name, opening_balance, currency_just_ILS)
    except ValueError as exception:
        raise_bad_request(str(exception))
    return {
        "id": account.id,
        "name": account.name,
        "opening_balance": account.opening_balance,
        "currency": account.currency,
        "is_deleted": account.is_deleted,
    }


@router.patch("/{account_id}")
async def edit_account_name(
    account_id: int, new_name: str, service: AccountServiceDep
) -> dict[str, Any]:
    try:
        account = await service.edit_account_name(account_id, new_name)

    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message:
            raise_not_found(message)
        raise_bad_request(message)
    return {
        "id": account.id,
        "name": account.name,
        "opening_balance": account.opening_balance,
        "currency": account.currency,
        "is_deleted": account.is_deleted,
    }


@router.delete("/{account_id}")
async def delete_account(account_id: int, service: AccountServiceDep) -> None:
    try:
        await service.delete_account(account_id)
    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message.strip():
            raise_not_found(message)
        raise_bad_request(message)


@router.get("/{account_id}/balance")
async def get_account_balance(
    account_id: int, service: AccountServiceDep
) -> dict[str, Decimal]:
    try:
        blance = await service.get_account_balance(account_id)

    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message.strip():
            raise_not_found(message)
        raise_bad_request(message)
    return {"balance": blance}


@router.get("/net-worth")
async def get_net_worth(service: AccountServiceDep) -> dict[str, Decimal]:
    try:
        net_worth = await service.net_worth()
    except ValueError as exception:
        raise_bad_request(str(exception))
    return {"net_worth": net_worth}
