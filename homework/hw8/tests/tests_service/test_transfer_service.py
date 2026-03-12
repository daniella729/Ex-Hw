from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from solution.models.models import Transfer, Account
from solution.services.transfer_service import TransferService


@pytest.fixture
def transfer_repository_mock() -> Mock:
    repository = Mock()
    transfers = {
        1: Transfer(
            id=1,
            description="Move money",
            amount=Decimal("200"),
            transfer_date=date(2025,1,2),
            created_at=date(2025, 1, 1),
            from_account_id=1,
            to_account_id=2,
            is_deleted=False,
        ),
        2: Transfer(
            id=2,
            description="Pay credit",
            amount=Decimal("300"),
            transfer_date=date(2025,1,2),
            created_at=date(2025, 1, 2),
            from_account_id=2,
            to_account_id=1,
            is_deleted=False,
        ),
    }
    repository.get_all.return_value = list(transfers.values())
    repository.get.side_effect = transfers.get
    return repository


@pytest.fixture
def account_repository_mock() -> Mock:
    repository = Mock()
    repository.get.return_value = Mock()

    return repository


@pytest.fixture
def transfer_service(
    transfer_repository_mock: Mock,
    account_repository_mock: Mock,
) -> TransferService:
    return TransferService(
        transfer_repository=transfer_repository_mock,
        account_repository=account_repository_mock,
    )

@pytest.mark.asyncio
async def test_get_all_transfers(
    transfer_service: TransferService,
) -> None:
    expected = [
        Transfer(
            id=1,
            description="Move money",
            amount=Decimal("200"),
            transfer_date=date(2025,1,2),
            created_at=date(2025, 1, 1),
            from_account_id=1,
            to_account_id=2,
            is_deleted=False,
        ),
        Transfer(
            id=2,
            description="Pay credit",
            amount=Decimal("300"),
            transfer_date=date(2025,1,2),
            created_at=date(2025, 1, 2),
            from_account_id=2,
            to_account_id=1,
            is_deleted=False,
        ),
    ]
    result = await transfer_service.get_all_transfer()
    assert result == expected

@pytest.mark.asyncio
async def test_add_transfer(
    transfer_service: TransferService,
    transfer_repository_mock: Mock,
    account_repository_mock: Mock,
) -> None:
    new_transfer = Transfer(
        id=3,
        description="Top up",
        amount=Decimal("100"),
        transfer_date=date(2025,1,2),
        created_at=date(2025, 1, 3),
        from_account_id=1,
        to_account_id=2,
        is_deleted=False,
    )

    transfer_repository_mock.create.return_value = new_transfer

    result = await transfer_service.add_transfer(
        description="Top up",
        amount=Decimal("100"),
        transfer_date=date(2025,1,2),
        from_account_id=1,
        to_account_id=2,
        
    )

    assert result == new_transfer
    transfer_repository_mock.create.assert_called_once()

@pytest.mark.asyncio
async def test_delete_transfer(
    transfer_service: TransferService,
    transfer_repository_mock: Mock,
) -> None:
    await transfer_service.delete_transfer(2)
    transfer_repository_mock.delete.assert_called_once_with(2)

@pytest.mark.asyncio
async def test_add_transfer_empty_description(
    transfer_service: TransferService,
) -> None:
    with pytest.raises(ValueError, match="Description cannot be empty"):
        await transfer_service.add_transfer(
            description="",
            amount=Decimal("100"),
            transfer_date=date(2025,1,2),
            from_account_id=1,
            to_account_id=2,
            
        )

@pytest.mark.asyncio
async def test_add_transfer_raises_invalid_amount(
    transfer_service: TransferService,
) -> None:
    with pytest.raises(ValueError, match="Amount must be greater than zero"):
        await transfer_service.add_transfer(
            description="Move",
            amount=Decimal("0"),
            transfer_date=date(2025,1,2),
            from_account_id=1,
            to_account_id=2,
           
        )

@pytest.mark.asyncio
async def test_add_transfer_raises_same_account(
    transfer_service: TransferService,
) -> None:
    with pytest.raises(
        ValueError,
        match="transfer must be between two different accounts",
    ):
       await transfer_service.add_transfer(
            description="Move",
            amount=Decimal("100"),
            transfer_date=date(2025,1,2),
            from_account_id=1,
            to_account_id=1,
            
        )
