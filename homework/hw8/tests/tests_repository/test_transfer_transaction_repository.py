from unittest.mock import Mock
from decimal import Decimal
from datetime import date
import pytest

from solution.repository.transaction_repository import TransactionRepository
from solution.repository.transfer_repository import TransferRepository

from solution.models.models import Transaction, Transfer


@pytest.fixture
def transaction_accessor_mock() -> Mock:
    accessor = Mock()
    accessor.read.return_value = [
        {
            "id": "1",
            "description": "Coffee",
            "amount": "10",
            "created_at": "2025-01-01",
            "category_id": "1",
            "account_id": "1",
            "is_deleted": "False",
        },
        {
            "id": "2",
            "description": "Groceries",
            "amount": "50",
            "created_at": "2025-01-02",
            "category_id": "1",
            "account_id": "1",
            "is_deleted": "False",
        },
    ]
    return accessor


@pytest.fixture
def transaction_repository(transaction_accessor_mock: Mock) -> TransactionRepository:
    return TransactionRepository(transaction_accessor_mock)


@pytest.fixture
def transfer_accessor_mock() -> Mock:
    accessor = Mock()
    accessor.read.return_value = [
        {
            "id": "1",
            "description": "Move money",
            "amount": "200",
            "transfer_date":"2025-01-02",
            "created_at": "2025-01-01",
            "from_account_id": "1",
            "to_account_id": "2",
            "is_deleted": "False",
        },
        {
            "id": "2",
            "description": "Pay credit",
            "amount": "300",
            "transfer_date":"2025-01-02",
            "created_at": "2025-01-02",
            "from_account_id": "1",
            "to_account_id": "2",
            "is_deleted": "False",
        },
    ]
    return accessor


@pytest.fixture
def transfer_repository(transfer_accessor_mock: Mock) -> TransferRepository:
    return TransferRepository(transfer_accessor_mock)


def test_transaction_get_all(
    transaction_repository: TransactionRepository,
    transaction_accessor_mock: Mock,
) -> None:
    result = transaction_repository.get_all()

    expected = [
        Transaction(
            id=1,
            description="Coffee",
            amount=Decimal("10"),
            created_at=date(2025, 1, 1),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
        Transaction(
            id=2,
            description="Groceries",
            amount=Decimal("50"),
            created_at=date(2025, 1, 2),
            category_id=1,
            account_id=1,
            is_deleted=False,
        ),
    ]

    assert result == expected
    transaction_accessor_mock.read.assert_called_once_with()


def test_transaction_create(
    transaction_repository: TransactionRepository,
    transaction_accessor_mock: Mock,
) -> None:
    new_transaction = Transaction(
        id=3,
        description="Bus",
        amount=Decimal("12.5"),
        created_at=date(2025, 1, 3),
        category_id=2,
        account_id=1,
        is_deleted=False,
    )

    transaction_repository.create(new_transaction)

    transaction_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "description": "Coffee",
                "amount": "10",
                "created_at": "2025-01-01",
                "category_id": "1",
                "account_id": "1",
                "is_deleted": "False",
            },
            {
                "id": "2",
                "description": "Groceries",
                "amount": "50",
                "created_at": "2025-01-02",
                "category_id": "1",
                "account_id": "1",
                "is_deleted": "False",
            },
            {
                "id": "3",
                "description": "Bus",
                "amount": "12.5",
                "created_at": "2025-01-03",
                "category_id": "2",
                "account_id": "1",
                "is_deleted": "False",
            },
        ]
    )


def test_transaction_update(
    transaction_repository: TransactionRepository,
    transaction_accessor_mock: Mock,
) -> None:
    updated_transaction = Transaction(
        id=1,
        description="Coffee Updated",
        amount=Decimal("11"),
        created_at=date(2025, 1, 1),
        category_id=1,
        account_id=1,
        is_deleted=False,
    )

    transaction_repository.update(updated_transaction)

    transaction_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "description": "Coffee Updated",
                "amount": "11",
                "created_at": "2025-01-01",
                "category_id": "1",
                "account_id": "1",
                "is_deleted": "False",
            },
            {
                "id": "2",
                "description": "Groceries",
                "amount": "50",
                "created_at": "2025-01-02",
                "category_id": "1",
                "account_id": "1",
                "is_deleted": "False",
            },
        ]
    )


def test_transaction_get(transaction_repository: TransactionRepository) -> None:
    result = transaction_repository.get(1)

    expected = Transaction(
        id=1,
        description="Coffee",
        amount=Decimal("10"),
        created_at=date(2025, 1, 1),
        category_id=1,
        account_id=1,
        is_deleted=False,
    )
    assert result == expected


def test_transaction_delete(
    transaction_repository: TransactionRepository,
    transaction_accessor_mock: Mock,
) -> None:
    transaction_repository.delete(1)

    transaction_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "description": "Coffee",
                "amount": "10",
                "created_at": "2025-01-01",
                "category_id": "1",
                "account_id": "1",
                "is_deleted": "True",
            },
            {
                "id": "2",
                "description": "Groceries",
                "amount": "50",
                "created_at": "2025-01-02",
                "category_id": "1",
                "account_id": "1",
                "is_deleted": "False",
            },
        ]
    )


def test_transfer_get_all(
    transfer_repository: TransferRepository,
    transfer_accessor_mock: Mock,
) -> None:
    result = transfer_repository.get_all()

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
            from_account_id=1,
            to_account_id=2,
            is_deleted=False,
        ),
    ]

    assert result == expected
    transfer_accessor_mock.read.assert_called_once_with()


def test_transfer_create(
    transfer_repository: TransferRepository,
    transfer_accessor_mock: Mock,
) -> None:
    new_transfer = Transfer(
        id=3,
        description="Top up",
        amount=Decimal("50"),
        transfer_date=date(2025,1,2),
        created_at=date(2025, 1, 3),
        from_account_id=2,
        to_account_id=1,
        is_deleted=False,
    )

    transfer_repository.create(new_transfer)

    transfer_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "description": "Move money",
                "amount": "200",
                "transfer_date":"2025-01-02",
                "created_at": "2025-01-01",
                "from_account_id": "1",
                "to_account_id": "2",
                "is_deleted": "False",
            },
            {
                "id": "2",
                "description": "Pay credit",
                "amount": "300",
                "transfer_date":"2025-01-02",
                "created_at": "2025-01-02",
                "from_account_id": "1",
                "to_account_id": "2",
                "is_deleted": "False",
            },
            {
                "id": "3",
                "description": "Top up",
                "amount": "50",
                "transfer_date":"2025-01-02",
                "created_at": "2025-01-03",
                "from_account_id": "2",
                "to_account_id": "1",
                "is_deleted": "False",
            },
        ]
    )


def test_transfer_update(
    transfer_repository: TransferRepository,
    transfer_accessor_mock: Mock,
) -> None:
    updated_transfer = Transfer(
        id=2,
        description="Pay credit UPDATED",
        amount=Decimal("333"),
        transfer_date=date(2025,1,2),
        created_at=date(2025, 1, 2),
        from_account_id=1,
        to_account_id=2,
        is_deleted=False,
    )

    transfer_repository.update(updated_transfer)

    transfer_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "description": "Move money",
                "amount": "200",
                "transfer_date":"2025-01-02",
                "created_at": "2025-01-01",
                "from_account_id": "1",
                "to_account_id": "2",
                "is_deleted": "False",
            },
            {
                "id": "2",
                "description": "Pay credit UPDATED",
                "amount": "333",
                "transfer_date":"2025-01-02",
                "created_at": "2025-01-02",
                "from_account_id": "1",
                "to_account_id": "2",
                "is_deleted": "False",
            },
        ]
    )


def test_transfer_get(transfer_repository: TransferRepository) -> None:
    result = transfer_repository.get(1)

    expected = Transfer(
        id=1,
        description="Move money",
        amount=Decimal("200"),
        transfer_date=date(2025,1,2),
        created_at=date(2025, 1, 1),
        from_account_id=1,
        to_account_id=2,
        is_deleted=False,
    )
    assert result == expected


def test_transfer_delete(
    transfer_repository: TransferRepository,
    transfer_accessor_mock: Mock,
) -> None:
    transfer_repository.delete(1)

    transfer_accessor_mock.write.assert_called_once_with(
        [
            {
                "id": "1",
                "description": "Move money",
                "amount": "200",
                "transfer_date":"2025-01-02",
                "created_at": "2025-01-01",
                "from_account_id": "1",
                "to_account_id": "2",
                "is_deleted": "True",
            },
            {
                "id": "2",
                "description": "Pay credit",
                "amount": "300",
                "transfer_date":"2025-01-02",
                "created_at": "2025-01-02",
                "from_account_id": "1",
                "to_account_id": "2",
                "is_deleted": "False",
            },
        ]
    )
