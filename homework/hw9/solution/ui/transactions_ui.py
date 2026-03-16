from solution.ui.api_client import request_and_print, request_json
from solution.ui.input_check import (
    check_decimal_input,
    check_input,
    check_int_input,
    check_choice_input,
)


class TransactionUI:
    """CLI UI that communicates with the transaction Planner API server."""

    def __init__(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Transactions Menu =====")
        print("1. View all transactions")
        print("2. Add income transaction")
        print("3. Add expense transaction")
        print("4. Delete transaction")
        print("5. Back\n")

    def handle_choice(self) -> None:
        choice = check_choice_input(
            "Choose an option: ",
            {"1", "2", "3", "4", "5"},
        )

        match choice:
            case "1":
                self.view_all_transactions()
            case "2":
                self.add_income_transaction()
            case "3":
                self.add_expense_transaction()
            case "4":
                self.delete_transaction()
            case "5":
                self.running = False

    def view_all_transactions(self) -> None:
        all_transactions = request_json("GET", "/transactions")
        if all_transactions is None:
            return
        if not all_transactions:
            print("No transaction found")
        for transaction in all_transactions:
            print(transaction)

    def add_income_transaction(self) -> None:
        account_id = check_int_input("Enter account id: ")
        description = check_input("Enter description: ")
        amount = check_decimal_input("Enter amount:")
        categories = request_json("GET", "/categories")
        if categories is not None:
            print("\nAvailable categories:")
            for category in categories:
                print(f"{category['id']} - {category['name']}")
        category_id = check_int_input("Enter category id: ")
        request_and_print(
            "POST",
            "/transactions/income",
            "Income transaction created successfullu",
            {
                "account_id": account_id,
                "description": description,
                "amount": amount,
                "category_id": category_id,
            },
        )

    def add_expense_transaction(self) -> None:
        account_id = check_int_input("Enter account id: ")
        description = check_input("Enter description: ")
        amount = check_decimal_input("Enter amount:")
        categories = request_json("GET", "/categories")
        if categories is not None:
            print("\nAvailable categories:")
            for category in categories:
                print(f"{category['id']} - {category['name']}")
        category_id = check_int_input("Enter category id: ")
        request_and_print(
            "POST",
            "/transactions/expense",
            "Expense transaction created successfullu",
            {
                "account_id": account_id,
                "description": description,
                "amount": amount,
                "category_id": category_id,
            },
        )

    def delete_transaction(self) -> None:
        transaction_id = check_int_input("Enter transaction id: ")
        request_and_print(
            "DELETE",
            f"/transactions/{transaction_id}",
            "transaction deleted successfully",
        )
