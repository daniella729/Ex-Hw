from solution.budget import BudgetPlanner

LINE_LENGTH = 40
SEPARATOR_LINE = "=" * LINE_LENGTH


def check_description(prompt: str) -> str:
    while True:
        value = input(prompt)
        if value == "":
            print("description cannot be empty.")
            continue
        return value


def check_amount(prompt: str) -> float:
    while True:
        value = input(prompt)
        if value == "":
            print("amount cannot be empty.")
            continue
        try:
            return float(value)
        except ValueError:
            print("please enter a valid number.")


class BudgetCLI:
    """Command line interface for interacting with the BudgetPlanner."""

    def __init__(self, planner: BudgetPlanner) -> None:
        self.planner = planner
        self.running = True

    def run(self) -> None:
        """Run the main CLI loop until the user exits."""
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Budget Planner =====")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Remove Income")
        print("5. Remove Expense")
        print("6. Clear All Data")
        print("7. Exit\n")

    def handle_choice(self) -> None:
        choice = input("Choose an option: ")
        if choice == "7":
            print("Goodbye!")
            self.running = False
            return

        match choice:
            case "1":
                self.add_income()
            case "2":
                self.add_expense()
            case "3":
                self.view_summary()
            case "4":
                self.remove_income()
            case "5":
                self.remove_expense()
            case "6":
                self.clear_all_data()
            case _:
                print("Invalid choice. Please try again.")

    def add_income(self) -> None:
        description = check_description("Enter income description: ")
        amount = check_amount("Enter income amount: ")
        result = self.planner.add_income(description, amount)
        print("Income added successfully!" if result is None else result)

    def add_expense(self) -> None:
        description = check_description("Enter expense description: ")
        amount = check_amount("Enter expense amount: ")
        result = self.planner.add_expense(description, amount)
        print("Expense added successfully!" if result is None else result)

    def remove_income(self) -> None:
        """
        Remove an income by description or by 1-based index.
        Why we call list_incomes() here:
        - The planner API removes by description.
        - If the user enters an index, we must translate it into a description.
        - We use planner.list_incomes() (service layer) instead of accessing the
        repository directly, to keep the CLI independent from data storage.
        """
        description = check_description("Enter income description/index to remove: ")
        if description.isdigit():
            income_index = int(description) - 1
            incomes = self.planner.list_incomes()
            if 0 <= income_index < len(incomes):
                description = incomes[income_index].description
            else:
                print("Invalid index.")
                return
        result = self.planner.remove_income(description)
        print(result if isinstance(result, str) else "Removed successfully!")

    def remove_expense(self) -> None:
        description = check_description("Enter expense description/index to remove: ")
        if description.isdigit():
            expense_index = int(description) - 1
            expenses = self.planner.list_expenses()
            if 0 <= expense_index < len(expenses):
                description = expenses[expense_index].description
            else:
                print("Invalid index.")
                return
        result = self.planner.remove_expense(description)
        print(result if isinstance(result, str) else "Removed successfully!")

    def clear_all_data(self) -> None:
        self.planner.clear_all_data()
        print("All data cleared.")

    def view_summary(self) -> None:
        summary = self.planner.get_summary()
        print(SEPARATOR_LINE, "\n            BUDGET SUMMARY")
        print(SEPARATOR_LINE, "\nINCOME SOURCES:")
        if summary["incomes"]:
            index = 1
            for income in summary["incomes"]:
                amount_str = f"${income.amount:.2f}"
                print(f"{index}. {income.description:<25} {amount_str:>11}")
                index += 1
        else:
            print("No incomes recorded.")
        print("\n", "-" * LINE_LENGTH)
        total_income_str = "${:.2f}".format(summary["total_income"])
        print("{:<28}{:>11}".format("TOTAL INCOME:", total_income_str))
        print("\nEXPENSES:")
        if summary["expenses"]:
            index = 1
            for expense in summary["expenses"]:
                amount_str = f"${expense.amount:.2f}"
                print(f"{index}. {expense.description:<25} {amount_str:>11}")
                index += 1
        else:
            print("No expenses recorded.")
        print("\n", "-" * LINE_LENGTH)
        total_expenses_str = "${:.2f}".format(summary["total_expenses"])
        print("{:<28}{:>11}".format("TOTAL EXPENSES:", total_expenses_str))
        print(SEPARATOR_LINE)
        net_balance_str = "${:.2f}".format(summary["net_balance"])
        print("{:<28}{:>11}".format("REMAINING BUDGET:", net_balance_str))
        print(SEPARATOR_LINE)
        input("\nPress Enter to return to the menu...")
