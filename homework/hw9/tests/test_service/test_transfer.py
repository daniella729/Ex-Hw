from datetime import date
from decimal import Decimal
from typing import cast
from unittest.mock import AsyncMock

import pytest

from solution.models.account import Account
from solution.models.transfer import Transfer
from solution.services.transfer_service import TransferService


@pytest.mark.asyncio
async def test_get_all_transfer(transfer_service: TransferService) -> None:
    transfers = [
        Transfer(
            id=1,
            description="Transfer to savings",
            amount=Decimal("500"),
            transfer_date=date(2026, 3, 1),
            created_at=date(2026, 3, 1),
            from_account_id=1,
            to_account_id=2,
            is_deleted=False,
        ),
        Transfer(
            id=2,
            description="Deleted transfer",
            amount=Decimal("100"),
            transfer_date=date(2026, 3, 2),
            created_at=date(2026, 3, 2),
            from_account_id=1,
            to_account_id=3,
            is_deleted=True,
        ),
    ]
    cast(
        AsyncMock,
        transfer_service.transfer_repository.get_all,
    ).return_value = transfers

    result = await transfer_service.get_all_transfer()

    assert len(result) == 1
    assert result[0].description == "Transfer to savings"


@pytest.mark.asyncio
async def test_add_transfer(transfer_service: TransferService) -> None:
    from_account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("1000"),
        currency="ILS",
        is_deleted=False,
    )
    to_account = Account(
        id=2,
        name="Savings",
        opening_balance=Decimal("500"),
        currency="ILS",
        is_deleted=False,
    )
    created_transfer = Transfer(
        id=5,
        description="Move to savings",
        amount=Decimal("300"),
        transfer_date=date(2026, 3, 15),
        created_at=date.today(),
        from_account_id=1,
        to_account_id=2,
        is_deleted=False,
    )

    get_mock = cast(AsyncMock, transfer_service.account_repository.get)
    get_mock.side_effect = [from_account, to_account]

    create_mock = cast(AsyncMock, transfer_service.transfer_repository.create)
    create_mock.return_value = created_transfer

    result = await transfer_service.add_transfer(
        description="Move to savings",
        amount=Decimal("300"),
        transfer_date=date(2026, 3, 15),
        from_account_id=1,
        to_account_id=2,
    )

    assert result.id == 5
    assert result.amount == Decimal("300")
    assert result.from_account_id == 1
    assert result.to_account_id == 2
    create_mock.assert_awaited_once()


@pytest.mark.parametrize(
    ("description", "amount", "from_account_id", "to_account_id"),
    [
        ("", Decimal("100"), 1, 2),
        ("Valid transfer", Decimal("0"), 1, 2),
        ("Valid transfer", Decimal("-5"), 1, 2),
        ("Valid transfer", Decimal("100"), 1, 1),
    ],
)
@pytest.mark.asyncio
async def test_add_transfer_invalid_data(
    transfer_service: TransferService,
    description: str,
    amount: Decimal,
    from_account_id: int,
    to_account_id: int,
) -> None:
    account = Account(
        id=1,
        name="Main",
        opening_balance=Decimal("1000"),
        currency="ILS",
        is_deleted=False,
    )
    second_account = Account(
        id=2,
        name="Savings",
        opening_balance=Decimal("2000"),
        currency="ILS",
        is_deleted=False,
    )

    get_mock = cast(AsyncMock, transfer_service.account_repository.get)
    get_mock.side_effect = [account, second_account]

    with pytest.raises(ValueError):
        await transfer_service.add_transfer(
            description=description,
            amount=amount,
            transfer_date=date(2026, 3, 15),
            from_account_id=from_account_id,
            to_account_id=to_account_id,
        )


@pytest.mark.asyncio
async def test_delete_transfer(transfer_service: TransferService) -> None:
    transfer = Transfer(
        id=1,
        description="Transfer to savings",
        amount=Decimal("200"),
        transfer_date=date(2026, 3, 10),
        created_at=date(2026, 3, 10),
        from_account_id=1,
        to_account_id=2,
        is_deleted=False,
    )
    cast(AsyncMock, transfer_service.transfer_repository.get).return_value = transfer

    await transfer_service.delete_transfer(transfer_id=1)

    delete_mock = cast(AsyncMock, transfer_service.transfer_repository.delete)
    delete_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_transfer_already_deleted(
    transfer_service: TransferService,
) -> None:
    transfer = Transfer(
        id=1,
        description="Deleted transfer",
        amount=Decimal("200"),
        transfer_date=date(2026, 3, 10),
        created_at=date(2026, 3, 10),
        from_account_id=1,
        to_account_id=2,
        is_deleted=True,
    )
    cast(AsyncMock, transfer_service.transfer_repository.get).return_value = transfer

    with pytest.raises(ValueError):
        await transfer_service.delete_transfer(transfer_id=1)
