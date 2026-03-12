from solution.ui.account_ui import AccountUI
from solution.ui.categories_ui import CategoryUI
from solution.ui.reports_ui import ReportUI
from solution.ui.transactions_ui import TransactionUI
from solution.ui.transfer_ui import TransferUI
from solution.ui.input_check import check_choice_input


class BudgetUI:
    """CLI UI that communicates with the Budget Planner API server."""

    def __init__(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Budget Planner Menu =====")
        print("1. Accounts")
        print("2. Categories")
        print("3. Transactions")
        print("4. Transfers")
        print("5. Reports")
        print("6. Exit\n")

    def handle_choice(self) -> None:
        choice = check_choice_input(
            "Choose an option: ",
            {"1", "2", "3", "4", "5", "6"},
        )
        match choice:
            case "1":
                AccountUI().run()
            case "2":
                CategoryUI().run()
            case "3":
                TransactionUI().run()
            case "4":
                TransferUI().run()
            case "5":
                ReportUI().run()
            case "6":
                print("Goodbye!")
                self.running = False

if __name__ == "__main__":
    ui = BudgetUI()
    ui.run()
