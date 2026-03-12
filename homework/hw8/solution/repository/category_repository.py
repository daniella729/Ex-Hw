from solution.models.models import Category, CategoryType
from solution.repository.base_repository import BaseRepository
from solution.repository.csv_accessor import CsvFileAccessor

ID = "id"
NAME = "name"


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, accessor: CsvFileAccessor):
        super().__init__(accessor, Category)

    def convert_data(self, row: dict[str, str]) -> Category:
        return Category(
            id=int(row[ID]),
            name=row[NAME],
            category_type=CategoryType(row["category_type"]),
            is_archived=row["is_archived"] == "True",
        )

    def data_to_row(self, item: Category) -> dict[str, str]:
        return {
            ID: str(item.id),
            NAME: item.name,
            "category_type": item.category_type.value,
            "is_archived": str(item.is_archived),
        }
