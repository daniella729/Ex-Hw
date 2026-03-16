from typing import Generic, TypeVar, Type, runtime_checkable, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ID = "id"
EntityType = TypeVar("EntityType")


@runtime_checkable
class Deletable(Protocol):
    is_deleted: bool


@runtime_checkable
class Archivable(Protocol):
    is_archived: bool


class BaseRepository(Generic[EntityType]):
    def __init__(self, model_type: Type[EntityType]) -> None:
        self._model_type = model_type

    async def create(self, session: AsyncSession, item: EntityType) -> EntityType:
        session.add(item)
        return item

    async def get(self, session: AsyncSession, item_id: int) -> EntityType:
        stmt = select(self._model_type).where(
            getattr(self._model_type, ID) == item_id,
        )
        result = await session.execute(stmt)
        item = result.scalar_one_or_none()
        if item is None:
            raise ValueError("Item not found")
        return item

    async def get_all(self, session: AsyncSession) -> list[EntityType]:
        stmt = select(self._model_type)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, session: AsyncSession, item: EntityType) -> EntityType:
        existing_item = await self.get(getattr(item, ID), session)

        for key, value in vars(item).items():
            setattr(existing_item, key, value)

        return existing_item

    async def delete(self, session: AsyncSession, item_id: int) -> None:
        stmt = select(self._model_type).where(
            getattr(self._model_type, ID) == item_id,
        )
        result = await session.execute(stmt)
        item = result.scalar_one_or_none()
        if item is None:
            raise ValueError("Item not found")
        if hasattr(item, "is_deleted"):
            setattr(item, "is_deleted", True)
        elif hasattr(item, "is_archived"):
            setattr(item, "is_archived", True)
        else:
            raise ValueError("Entity does not support soft delete")
        session.add(item)
