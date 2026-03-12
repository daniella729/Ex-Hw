from solution.models.models import Category, CategoryType
from solution.repository.category_repository import CategoryRepository
from solution.repository.transaction_repository import TransactionRepository

FIRST_GENERATED_ID = 1


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        transaction_repository: TransactionRepository,
    ) -> None:
        self.category_repository = category_repository
        self.transaction_repository = transaction_repository

    async def add_category(self, name: str, category_type: CategoryType) -> Category:
        self.validate_category_name(name)
        category = Category(
            id=self.generate_category_id(),
            name=name,
            category_type=category_type,
        )
        return self.category_repository.create(category)

    async def delete_category(self, category_id: int) -> None:
        category = self.category_repository.get(category_id)
        if category.is_archived:
            raise ValueError("Category already archived")
        if self.category_has_transaction(category_id):
            raise ValueError("Cannot delete category that has a transaction")
        self.category_repository.delete(category_id)

    async def get_all_category(self) -> list[Category]:
        categories = self.category_repository.get_all()
        return [category for category in categories if not category.is_archived]

    def generate_category_id(self) -> int:
        categories = self.category_repository.get_all()
        active_categories = [
            category for category in categories if not category.is_archived
        ]
        if active_categories:
            return max(transfer.id for transfer in categories) + 1
        else:
            return FIRST_GENERATED_ID

    def validate_category_name(self, name: str) -> None:
        if name == "":
            raise ValueError("Category name cannot be empty")

    def category_has_transaction(self, category_id: int) -> bool:
        transactions = self.transaction_repository.get_all()
        for transaction in transactions:
            if transaction.is_deleted:
                continue
            if transaction.category_id == category_id:
                return True
        return False
