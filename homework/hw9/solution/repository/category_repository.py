from solution.repository.base_repository import BaseRepository
from solution.models.category import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self) -> None:
        super().__init__(Category)
