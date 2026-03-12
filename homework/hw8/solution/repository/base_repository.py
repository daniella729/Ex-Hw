from typing import Generic, TypeVar, Type, runtime_checkable
from solution.repository.csv_accessor import CsvFileAccessor
from typing import Protocol

ID = "id"
EntityType = TypeVar("EntityType")


@runtime_checkable
class Deletable(Protocol):
    is_deleted: bool


@runtime_checkable
class Archivable(Protocol):
    is_archived: bool


class BaseRepository(Generic[EntityType]):
    def __init__(self, accessor: CsvFileAccessor, model_type: Type[EntityType]) -> None:
        self._accessor = accessor
        self._model_type = model_type

    def convert_data(self, row: dict[str, str]) -> EntityType:
        raise NotImplementedError

    def data_to_row(self, item: EntityType) -> dict[str, str]:
        raise NotImplementedError

    def create(self, item: EntityType) -> EntityType:
        rows = self._accessor.read()
        row = self.data_to_row(item)
        rows.append(row)
        self._accessor.write(rows)
        return item

    def get(self, item_id: int) -> EntityType:
        rows = self._accessor.read()
        for row in rows:
            if int(row[ID]) == item_id:
                return self.convert_data(row)
        raise ValueError("Item not found")

    def get_all(self) -> list[EntityType]:
        rows = self._accessor.read()
        return [self.convert_data(row) for row in rows]

    def update(self, item: EntityType) -> EntityType:
        rows = self._accessor.read()
        update_rows = []
        found = False
        for row in rows:
            if int(row[ID]) == getattr(item, ID):
                update_rows.append(self.data_to_row(item))
                found = True
            else:
                update_rows.append(row)
        if found is False:
            raise ValueError("Item not found")
        self._accessor.write(update_rows)
        return item

    def delete(self, item_id: int) -> None:
        rows = self._accessor.read()

        for row in rows:
            if int(row[ID]) == item_id:
                item = self.convert_data(row)

                if isinstance(item, Deletable):
                    item.is_deleted = True
                elif isinstance(item, Archivable):
                    item.is_archived = True
                else:
                    raise ValueError("Entity does not support soft delete")

                row.update(self.data_to_row(item))
                self._accessor.write(rows)
                return

        raise ValueError("Item not found")
