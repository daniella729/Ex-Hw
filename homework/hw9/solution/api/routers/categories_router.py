from typing import Annotated, Any
from fastapi import APIRouter, Depends
from solution.api.dependencies import (
    get_category_service,
    raise_bad_request,
    raise_not_found,
)

NOT_FOUND = "not found"
from solution.models.category import CategoryType
from solution.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])
CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]


@router.get("", response_model=list[dict[str, Any]])
async def get_all_catrgories(service: CategoryServiceDep) -> list[dict[str, Any]]:
    try:
        categories = await service.get_all_category()
        return [
            {
                "id": category.id,
                "name": category.name,
                "category_type": category.category_type,
                "is_archived": category.is_archived,
            }
            for category in categories
        ]
    except ValueError as exception:
        raise_bad_request(str(exception))


@router.post("")
async def add_category(
    name: str, category_type: CategoryType, service: CategoryServiceDep
) -> dict[str, Any]:
    try:
        category = await service.add_category(name, category_type)
    except ValueError as exception:
        raise_bad_request(str(exception))
    return {
        "id": category.id,
        "name": category.name,
        "category_type": category.category_type,
        "is_archived": category.is_archived,
    }


@router.delete("/{category_id}")
async def delete_category(category_id: int, service: CategoryServiceDep) -> None:
    try:
        await service.delete_category(category_id)
    except ValueError as exception:
        message = str(exception)
        if NOT_FOUND in message.strip():
            raise_not_found(message)
        raise_bad_request(message)
