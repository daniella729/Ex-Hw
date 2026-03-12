from solution.repository.transaction_repository import TransactionRepository
from solution.repository.category_repository import CategoryRepository
from solution.models.models import CategoryType
from decimal import Decimal
INVAILD_VALUE=0
class ReportService:
    def __init__(self,transaction_repository:TransactionRepository,category_repository:CategoryRepository)->None:
        self.transaction_repository=transaction_repository
        self.category_repository=category_repository

    async def get_spending_breakdown_by_category(
    self, month: int, year: int
     ) -> list[dict[str, str | Decimal]]:
      transactions = self.transaction_repository.get_all()
      result:dict[str,Decimal]={}
      for transaction in transactions:
        if transaction.is_deleted or transaction.created_at.month != month or transaction.created_at.year != year:
            continue
        category=self.category_repository.get(transaction.category_id)
        if category.category_type!=CategoryType.EXPENSE:
            continue
        if category.name  not in result:
            result[category.name]=Decimal(INVAILD_VALUE)
        result[category.name]=result[category.name]+transaction.amount
        
      return[{
            "category":category_name,"total spending":amount 
         } for category_name ,amount in result.items()]
