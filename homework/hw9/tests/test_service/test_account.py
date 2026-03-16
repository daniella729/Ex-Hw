from decimal import Decimal
from typing import Any, cast
from sqlalchemy.exc import IntegrityError
from solution.models.account import Account
from solution.services.account_service import AccountService
from unittest.mock import AsyncMock
import pytest


def account_to_dict(account: Account | None) -> dict[str, Any]:
    if account is None:
        return {}
    return {
        "account_id": account.id,
        "account_name": account.name,
        "opening_opening_balance": account.opening_balance,
        "currency": account.currency,
    }


@pytest.mark.asyncio
async def test_show_all_accounts(account_service: AccountService) -> None:
    accounts_test = [
        Account(
            id=1,
            name="Main",
            opening_balance=Decimal("5000"),
            currency="ILS",
            is_deleted=False,
        ),
        Account(
            id=3,
            name="Home",
            opening_balance=Decimal("1500"),
            currency="ILS",
            is_deleted=False,
        ),
        Account(
            id=4,
            name="Car",
            opening_balance=Decimal("0"),
            currency="ILS",
            is_deleted=False,
        ),
        Account(
            id=5,
            name="Trip",
            opening_balance=Decimal("1234"),
            currency="ILS",
            is_deleted=False,
        ),
    ]
    result = await account_service.get_all_account_with_current_balance()
    assert len(result) == len(accounts_test)


@pytest.mark.asyncio
async def test_add_account_with_empty_name(account_service: AccountService) -> None:
    with pytest.raises(ValueError):
        await account_service.add_account(
            "",
            Decimal("123"),
            currency="ILS",
        )


@pytest.mark.asyncio
async def test_add_account_with_negative_balance(
    account_service: AccountService,
) -> None:
    with pytest.raises(ValueError):
        await account_service.add_account(
            "Main",
            Decimal("-1"),
            currency="ILS",
        )


@pytest.mark.asyncio
async def test_add_new_account(account_service: AccountService) -> None:
    created_account = Account(
        id=1,
        name="test",
        opening_balance=Decimal("123"),
        currency="ILS",
        is_deleted=False,
    )
    cast(AsyncMock, account_service.account_repository.create).return_value = (
        created_account
    )

    result = await account_service.add_account("test", Decimal("123"), currency="ILS")

    assert result.id == 1
    assert result.name == "test"
    assert result.opening_balance == Decimal("123")
    assert result.currency == "ILS"

    create_mock = cast(AsyncMock, account_service.account_repository.create)
    create_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_edit_account_name(account_service: AccountService) -> None:
    existing_account = Account(
        id=1,
        name="test",
        opening_balance=Decimal("123"),
        currency="ILS",
        is_deleted=False,
    )
    get_mock = cast(AsyncMock, account_service.account_repository.get)
    get_mock.return_value = existing_account

    update_mock = cast(AsyncMock, account_service.account_repository.update)
    update_mock.return_value = existing_account

    result = await account_service.edit_account_name(
        account_id=1,
        new_name="new_name",
    )
    assert result.name == "new_name"
    get_mock.assert_awaited_once()
    update_mock.assert_awaited_once()


@pytest.mark.parametrize(
    ("account_id", "new_name"),
    [
        ("", "Main"),
        (1, ""),
    ],
)
@pytest.mark.asyncio
async def test_empty_account_name_empty(
    account_service: AccountService, account_id: int, new_name: str
) -> None:
    with pytest.raises(ValueError):
        await account_service.edit_account_name(account_id, new_name)


@pytest.mark.asyncio
async def test_delete_account(account_service: AccountService) -> None:
    account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("5000"),
        currency="ILS",
        is_deleted=False,
    )

    cast(AsyncMock, account_service.account_repository.get).return_value = account
    cast(
        AsyncMock,
        account_service.transaction_repository.get_all,
    ).return_value = []
    cast(
        AsyncMock,
        account_service.transfer_repository.get_all,
    ).return_value = []

    await account_service.delete_account(account_id=1)

    delete_mock = cast(AsyncMock, account_service.account_repository.delete)
    delete_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_account_balance(account_service: AccountService) -> None:
    account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("5000"),
        currency="ILS",
        is_deleted=False,
    )
    cast(
        AsyncMock,
        account_service.account_repository.get,
    ).return_value = account

    cast(
        AsyncMock,
        account_service.transaction_repository.get_all,
    ).return_value = []

    cast(
        AsyncMock,
        account_service.transfer_repository.get_all,
    ).return_value = []

    result = await account_service.get_account_balance(account_id=1)

    assert result == Decimal("5000")


@pytest.mark.asyncio
async def test_net_worth(account_service: AccountService) -> None:
    cast(
        AsyncMock,
        account_service.transaction_repository.get_all,
    ).return_value = []

    cast(
        AsyncMock,
        account_service.transfer_repository.get_all,
    ).return_value = []

    cast(AsyncMock, account_service.account_repository.get).side_effect = [
        Account(
            id=1,
            name="Main",
            opening_balance=Decimal("5000"),
            currency="ILS",
            is_deleted=False,
        ),
        Account(
            id=3,
            name="Home",
            opening_balance=Decimal("1500"),
            currency="ILS",
            is_deleted=False,
        ),
        Account(
            id=4,
            name="Car",
            opening_balance=Decimal("0"),
            currency="ILS",
            is_deleted=False,
        ),
        Account(
            id=5,
            name="Trip",
            opening_balance=Decimal("1234"),
            currency="ILS",
            is_deleted=False,
        ),
    ]

    result = await account_service.net_worth()

    assert result == Decimal("7734")
