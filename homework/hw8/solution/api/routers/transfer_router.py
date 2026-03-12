from datetime import date
from decimal import Decimal
from typing import Annotated, Any

from fastapi import APIRouter, Depends

from solution.api.dependencies import (
    get_transfer_service,
    raise_bad_request,
    raise_not_found,
)
from solution.services.transfer_service import TransferService

NOT_FOUND = "not found"

router = APIRouter(prefix="/transfers", tags=["Transfers"])

TransferServiceDep = Annotated[
    TransferService,
    Depends(get_transfer_service),
]
@router.get("", response_model=list)
async def get_all_transfers(
    service: TransferServiceDep,
) -> list:
    try:
        return await service.get_all_transfer()
    except ValueError as exception:
        raise_bad_request(str(exception))

@router.post("")
async def add_transfer(
    description: str,
    amount: Decimal,
    transfer_date:date,
    from_account_id: int,
    to_account_id: int,
    service: TransferServiceDep,
) -> dict[str, Any]:
    try:
        transfer = await service.add_transfer(
           description, amount, transfer_date,from_account_id,to_account_id
        )

    except ValueError as exception:
        raise_bad_request(str(exception))

    return {
        "id":transfer.id,
        "description": transfer.description,
        "amount":transfer.amount,
        "transfer_date":transfer.transfer_date,
        "created_at": transfer.created_at,
        "from_account_id": transfer.from_account_id,
        "to_account_id":transfer.to_account_id,
        "is_deleted": transfer.is_deleted,
        
    }
@router.delete("/{transfer_id}")
async def delete_transfer(transfer_id: int, service: TransferServiceDep) -> None:
    try:
        await service.delete_transfer(transfer_id)
    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message.strip():
            raise_not_found(message)
        raise_bad_request(message)
