from typing import Any
from fastapi import FastAPI
from solution.budget import BudgetPlanner, TransactionRepository, SummaryCalculator

MESSAGE = "message"
ERROR = "error"
DESCRIPTION = "description"
AMOUNT = "amount"
app = FastAPI(title="Budget planner API", description="Budget planner REST API")

repository = TransactionRepository()
calculator = SummaryCalculator()
planner = BudgetPlanner(repository, calculator)


@app.post("/income/{description}/{amount}")
async def add_new_income(description: str, amount: float) -> dict[str, Any]:
    result = planner.add_income(description, amount)
    if isinstance(result, str):
        return {ERROR: result}
    return {
        MESSAGE: "Income added successfully",
        DESCRIPTION: description,
        AMOUNT: amount,
    }


@app.delete("/income/{id}")
async def remove_income_by_id(id: str) -> dict[str, Any]:
    result = planner.remove_income(id)
    if isinstance(result, str):
        return {ERROR: result}
    return {
        MESSAGE: "Income removed successfully",
        DESCRIPTION: result.description,
        AMOUNT: result.amount,
    }


@app.post("/expense/{description}/{amount}")
async def add_expense(description: str, amount: float) -> dict[str, Any]:
    result = planner.add_expense(description, amount)
    if isinstance(result, str):
        return {ERROR: result}
    return {
        MESSAGE: "Expense added successfully",
        DESCRIPTION: description,
        AMOUNT: amount,
    }


@app.delete("/expense/{id}")
async def remove_expense_by_id(id: str) -> dict[str, Any]:
    result = planner.remove_expense(id)
    if isinstance(result, str):
        return {ERROR: result}
    return {
        MESSAGE: "Expense removed successfully",
        DESCRIPTION: result.description,
        AMOUNT: result.amount,
    }


@app.get("/summary")
async def get_summary() -> dict[str, Any]:
    return planner.get_summary()


@app.delete("/clear")
async def clear() -> dict[str, Any]:
    planner.clear_all_data()
    return {MESSAGE: "All data cleared"}
