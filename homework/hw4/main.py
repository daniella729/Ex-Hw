from solution.budget import (
    BudgetPlanner,
    TransactionRepository,
    SummaryCalculator,
)

from solution.cli import BudgetCLI


def main() -> None:
    repository = TransactionRepository()
    calculator = SummaryCalculator()
    planner = BudgetPlanner(repository, calculator)

    BudgetCLI(planner).run()


if __name__ == "__main__":
    main()
