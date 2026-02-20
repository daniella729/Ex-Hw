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


@pytest.fixture()
def planner() -> BudgetPlanner:
    repository = TransactionRepository()
    calculator = SummaryCalculator()
    return BudgetPlanner(repository, calculator)


def test_add_income_adds_to_repository(planner: BudgetPlanner) -> None:
    result = planner.add_income(SALARY, 5000)

    assert result is None
    incomes = planner.repository.list_incomes()
    assert len(incomes) == 1
    assert incomes[0] == Income(SALARY, 5000)


def test_add_expense_adds_to_repository(planner: BudgetPlanner) -> None:
    result = planner.add_expense("Rent", 1500)

    assert result is None
    expenses = planner.repository.list_expenses()
    assert len(expenses) == 1
    assert expenses[0] == Expense("Rent", 1500)


def test_add_income_empty_description(planner: BudgetPlanner) -> None:
    result = planner.add_income("", 10)

    assert result == ERROR_MEESAGE
    assert planner.repository.list_incomes() == []


def test_add_income_negative_amount(planner: BudgetPlanner) -> None:
    result = planner.add_income(SALARY, -1)

    assert result == "Amount cannot be negative"
    assert planner.repository.list_incomes() == []


def test_add_expense_empty_description(planner: BudgetPlanner) -> None:
    result = planner.add_expense("", 10)

    assert result == ERROR_MEESAGE
    assert planner.repository.list_expenses() == []


def test_add_expense_negative_amount(planner: BudgetPlanner) -> None:
    result = planner.add_expense("Rent", -1)

    assert result == "Amount cannot be negative"
    assert planner.repository.list_expenses() == []


def test_remove_income_empty_description(planner: BudgetPlanner) -> None:
    removed = planner.remove_income("")

    assert removed == ERROR_MEESAGE


def test_remove_income_returns_not_found(planner: BudgetPlanner) -> None:
    removed = planner.remove_income(SALARY)

    assert removed == "Income not found"


@pytest.mark.parametrize(
    ("seed_income", "expected"),
    [
        (True, 6000),
        (False, "Income not found"),
    ],
)
def test_update_income(
    planner: BudgetPlanner, seed_income: bool, expected: int | str
) -> None:
    if seed_income:
        planner.add_income("Salary", 5000)

    result = planner.repository.update_income("Salary", 6000)

    if isinstance(expected, int):
        assert isinstance(result, Income)
        assert result.amount == expected
        assert planner.repository.list_incomes()[0].amount == expected
    else:
        assert result == expected
