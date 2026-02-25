import pytest

from solution.budget import (
    BudgetPlanner,
    Expense,
    Income,
    SummaryCalculator,
    TransactionRepository,
)

SALARY = "Salary"
ERROR_MEESAGE = "Description cannot be empty"


@pytest.fixture
def budget_planner() -> BudgetPlanner:
    repository = TransactionRepository()
    calculator = SummaryCalculator()
    planner = BudgetPlanner(repository, calculator)
    return planner


def test_add_income_adds_to_repository(budget_planner: BudgetPlanner) -> None:
    result = budget_planner.add_income(SALARY, 5000)
    assert result is None
    incomes = budget_planner.repository.list_incomes()
    assert len(incomes) == 1
    assert incomes[0] == Income(SALARY, 5000)


def test_add_expense_adds_to_repository(budget_planner: BudgetPlanner) -> None:
    result = budget_planner.add_expense("Rent", 1500)

    assert result is None
    expenses = budget_planner.repository.list_expenses()
    assert len(expenses) == 1 and expenses[0] == Expense("Rent", 1500)


def test_add_income_empty_description(budget_planner: BudgetPlanner) -> None:
    result = budget_planner.add_income("", 10)

    assert result == ERROR_MEESAGE
    assert budget_planner.repository.list_incomes() == []


def test_add_income_negative_amount(budget_planner: BudgetPlanner) -> None:
    result = budget_planner.add_income(SALARY, -1)

    assert result == "Amount cannot be negative"
    assert budget_planner.repository.list_incomes() == []


def test_add_expense_empty_description(budget_planner: BudgetPlanner) -> None:
    result = budget_planner.add_expense("", 10)

    assert result == ERROR_MEESAGE
    assert budget_planner.repository.list_expenses() == []


def test_add_expense_negative_amount(budget_planner: BudgetPlanner) -> None:
    result = budget_planner.add_expense("Rent", -1)

    assert result == "Amount cannot be negative"
    assert budget_planner.repository.list_expenses() == []


def test_remove_income_empty_description(budget_planner: BudgetPlanner) -> None:
    removed = budget_planner.remove_income("")

    assert removed == ERROR_MEESAGE


def test_remove_income_returns_not_found(budget_planner: BudgetPlanner) -> None:
    removed = budget_planner.remove_income(SALARY)

    assert removed == "Income not found"


def test_update_income(budget_planner: BudgetPlanner) -> None:

    budget_planner.add_income("Salary", 5000)
    result = budget_planner.repository.update_income("Salary", 6000)
    assert isinstance(result, Income)
    assert result.amount == 6000
    assert budget_planner.repository.list_incomes()[0].amount == 6000
