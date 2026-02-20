from typing import Any

import requests

API_BASE_URL = "http://localhost:8000"
ERROR_KEY = "error"

HTTP_OK = 200

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


def request_json(method: str, path: str) -> Any | None:
    """Perform an HTTP request and return parsed JSON (or None on error)."""
    try:
        response = requests.request(method, f"{API_BASE_URL}{path}")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Is the server running?")
        return None

    if response.status_code != HTTP_OK:
        print(f"API error ({response.status_code})")
        return None

    try:
        data = response.json()
    except ValueError:
        print("Invalid response from API")
        return None

    if isinstance(data, dict) and ERROR_KEY in data:
        error_value = data.get(ERROR_KEY)
        print(
            error_value if isinstance(error_value, str) else "Invalid response from API"
        )
        return None

    return data


def request_and_print(
    method: str, path: str, success_message: str
) -> dict[str, Any] | None:
    """
    Call the API and print a success message only if the request succeeded.

    We keep printing decisions here so UI methods stay short and readable.
    """
    data = request_json(method, path)
    if data is None:
        return None

    print(success_message)
    return data if isinstance(data, dict) else None


class BudgetUI:
    """CLI UI that communicates with the Budget Planner API server."""

    def __init__(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Budget Planner UI =====")
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
                self.clear_all()
            case _:
                print("Invalid choice. Please try again.")

    def add_income(self) -> None:
        description = check_description("Enter income description: ")
        amount = check_amount("Enter income amount: ")
        request_and_print(
            "POST",
            f"/income/{description}/{amount}",
            "Income added successfully!",
        )

    def add_expense(self) -> None:
        description = check_description("Enter expense description: ")
        amount = check_amount("Enter expense amount: ")
        request_and_print(
            "POST",
            f"/expense/{description}/{amount}",
            "Expense added successfully!",
        )

    def remove_income(self) -> None:
        """
        Remove income by description OR by 1-based index.

        Why we fetch /summary for index deletion:
        - The API delete endpoint expects an identifier (here: description).
        - If the user enters an index, the UI must translate index -> description.
        - The UI should not keep its own copy of data; the server is the source of truth.
        """
        value = check_description("Enter income description/index to remove: ")
        request_and_print(
            "DELETE",
            f"/income/{value}",
            "Removed successfully!",
        )

    def remove_expense(self) -> None:
        value = check_description("Enter expense description/index to remove: ")
        request_and_print(
            "DELETE",
            f"/expense/{value}",
            "Removed successfully!",
        )

    def clear_all(self) -> None:
        request_and_print(
            "DELETE",
            "/clear",
            "All data cleared.",
        )

    def view_summary(self) -> None:
        summary = request_json("GET", "/summary")
        if not isinstance(summary, dict):
            print("Invalid response from API")
            return

        incomes = summary.get("incomes", [])
        expenses = summary.get("expenses", [])

        print(SEPARATOR_LINE, "\n            BUDGET SUMMARY")
        print(SEPARATOR_LINE, "\nINCOME SOURCES:")

        if incomes:
            for index, income in enumerate(incomes, start=1):
                print(f"{index}. {income['description']:<25} ${income['amount']:.2f}")
        else:
            print("No incomes recorded.")

        print("\nEXPENSES:")
        if expenses:
            for index, expense in enumerate(expenses, start=1):
                print(f"{index}. {expense['description']:<25} ${expense['amount']:.2f}")
        else:
            print("No expenses recorded.")

        print(SEPARATOR_LINE)
        print(f"TOTAL INCOME:     ${summary['total_income']:.2f}")
        print(f"TOTAL EXPENSES:   ${summary['total_expenses']:.2f}")
        print(f"REMAINING BUDGET: ${summary['net_balance']:.2f}")
        print(SEPARATOR_LINE)

        input("\nPress Enter to return to the menu...")
