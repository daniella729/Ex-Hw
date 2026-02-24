import pytest

from solution.budget import (
    BudgetPlanner,
    Expense,
    Income,
    SummaryCalculator,
    TransactionRepository,
)

SALARY = "Salary"


def test_get_summary_calculates_totals() -> None:
    repository = TransactionRepository()
    calculator = SummaryCalculator()
    planner = BudgetPlanner(repository, calculator)

    planner.add_income(SALARY, 5000)
    planner.add_income("Freelance", 1500)
    planner.add_expense("Rent", 1500)
    planner.add_expense("Groceries", 400)

    summary = planner.get_summary()

    assert summary["total_income"] == 6500
    assert summary["total_expenses"] == 1900
    assert summary["net_balance"] == 4600

    assert summary["incomes"] == [Income(SALARY, 5000), Income("Freelance", 1500)]
    assert summary["expenses"] == [Expense("Rent", 1500), Expense("Groceries", 400)]


def test_clear_all_removes_all_data() -> None:
    repository = TransactionRepository()
    calculator = SummaryCalculator()
    planner = BudgetPlanner(repository, calculator)

    planner.add_income(SALARY, 5000)
    planner.add_expense("Groceries", 1500)

    planner.clear_all_data()

    assert planner.repository.list_incomes() == []
    assert planner.repository.list_expenses() == []
