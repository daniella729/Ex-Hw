from dataclasses import dataclass
from typing import Any

ERROR_MEESAGE = "Description cannot be empty"
ZERO_AMOUNT = float(0)


@dataclass
class Expense:
    """represten a single expense entry"""

    description: str
    amount: float


@dataclass
class Income:
    """Represents a single income entry."""

    description: str
    amount: float


class TransactionRepository:
    """Stores and manages income and expense transactions."""

    def __init__(self) -> None:
        self.incomes: list[Income] = []
        self.expenses: list[Expense] = []

    def add_income(self, income: Income) -> None:
        self.incomes.append(income)

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)

    def list_incomes(self) -> list[Income]:
        return self.incomes

    def list_expenses(self) -> list[Expense]:
        return self.expenses

    def remove_income(self, description: str) -> Income | str:
        for income in self.incomes:
            if income.description == description:
                self.incomes.remove(income)
                return income
        return "Income not found"

    def remove_expense(self, description: str) -> Expense | str:
        for expense in self.expenses:
            if expense.description == description:
                self.expenses.remove(expense)
                return expense

        return "expense not found"

    def update_income(self, description: str, new_amount: float) -> Income | str:
        for income in self.incomes:
            if income.description == description:
                income.amount = new_amount
                return income

        return "Income not found"

    def update_expense(self, description: str, new_amount: float) -> Expense | str:
        for expense in self.expenses:
            if expense.description == description:
                expense.amount = new_amount
                return expense

        return "expense not found"

    def clear_all(self) -> None:
        self.incomes.clear()
        self.expenses.clear()


class SummaryCalculator:
    """Calculates totals and balances for transactions."""

    def total_income(self, incomes: list[Income]) -> float:
        total_income = ZERO_AMOUNT
        for income in incomes:
            total_income = total_income + income.amount
        return total_income

    def total_expense(self, expenses: list[Expense]) -> float:
        total_expense = ZERO_AMOUNT
        for expense in expenses:
            total_expense = total_expense + expense.amount
        return total_expense

    def net_balance(self, expenses: list[Expense], incomes: list[Income]) -> float:
        income_total = self.total_income(incomes)
        expense_total = self.total_expense(expenses)
        net_balance = income_total - expense_total
        return net_balance


class BudgetPlanner:
    """Service layer for budget operations."""

    def __init__(
        self, repository: TransactionRepository, calculator: SummaryCalculator
    ) -> None:
        self.repository = repository
        self.calculator = calculator

    def add_income(self, description: str, amount: float) -> None | str:
        if description == "":
            return ERROR_MEESAGE
        elif amount < 0:
            return "Amount cannot be negative"
        else:
            income = Income(description, amount)
            self.repository.add_income(income)
            return None

    def add_expense(self, description: str, amount: float) -> None | str:
        if description == "":
            return ERROR_MEESAGE
        elif amount < 0:
            return "Amount cannot be negative"
        else:
            expense = Expense(description, amount)
            self.repository.add_expense(expense)
            return None

    def remove_income(self, description: str) -> Income | str:
        if description == "":
            return ERROR_MEESAGE
        removed_income = self.repository.remove_income(description)
        return removed_income

    def remove_expense(self, description: str) -> Expense | str:
        if description == "":
            return ERROR_MEESAGE
        removed_expense = self.repository.remove_expense(description)
        return removed_expense

    def get_summary(self) -> dict[str, Any]:
        incomes = self.repository.list_incomes()
        expenses = self.repository.list_expenses()

        total_income = self.calculator.total_income(incomes)
        total_expenses = self.calculator.total_expense(expenses)
        net = self.calculator.net_balance(expenses, incomes)

        return {
            "incomes": incomes,
            "expenses": expenses,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_balance": net,
        }

    def clear_all_data(self) -> None:
        self.repository.clear_all()

    def list_incomes(self) -> list[Income]:
        """
        Returns incomes through the service layer.

        This keeps the CLI (or API layer) independent from the repository.
        The planner acts as a mediator between layers.
        """
        return self.repository.list_incomes()

    def list_expenses(self) -> list[Expense]:
        """
        Returns incomes through the service layer."""

        return self.repository.list_expenses()
