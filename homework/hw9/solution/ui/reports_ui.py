from solution.ui.api_client import request_and_print, request_json
from solution.ui.input_check import (
    check_decimal_input,
    check_input,
    check_int_input,
    check_choice_input,
    check_date_input,
)


class ReportUI:
    """CLI UI that communicates with the report Planner API server."""

    def __init__(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Reports Menu =====")
        print("1. Spending breakdown by category")
        print("2. Back\n")

    def handle_choice(self) -> None:
        choice = check_choice_input(
            "Choose an option: ",
            {"1", "2"},
        )
        match choice:
            case "1":
                self.view_spending_by_category()
            case "2":
                self.running = False

    def view_spending_by_category(self) -> None:
        month = check_int_input("Enter month: ")
        year = check_int_input("Enter year: ")
        data = request_json(
            "GET",
            "/reports/spending-by-category",
            {"month": month, "year": year},
        )
        if data is None:
            return
        if not data:
            print("No spending data found")
        print(data)
