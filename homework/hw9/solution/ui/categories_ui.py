from solution.ui.api_client import request_and_print, request_json
from solution.ui.input_check import (
    check_decimal_input,
    check_input,
    check_int_input,
    check_choice_input,
)


class CategoryUI:
    """CLI UI that communicates with the Category Planner API server."""

    def __init__(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Categories Menu =====")
        print("1. View all category")
        print("2. Add  category")
        print("3. Delete category")
        print("4. Back\n")

    def handle_choice(self) -> None:
        choice = check_choice_input(
            "Choose an option: ",
            {"1", "2", "3", "4"},
        )

        match choice:
            case "1":
                self.view_all_categories()
            case "2":
                self.add_category()
            case "3":
                self.delete_category()
            case "4":
                self.running = False

    def view_all_categories(self) -> None:
        all_categories = request_json("GET", "/categories")
        if all_categories is None:
            return
        if not all_categories:
            print("No categories found")
        for categorey in all_categories:
            print(categorey)

    def add_category(self) -> None:
        name = check_input("Enter category name: ")
        category_type = check_choice_input(
            "Enter category type (income/expense): ", {"income", "expense"}
        )
        request_and_print(
            "POST",
            "/categories",
            "Category created successfully",
            {"name": name, "category_type": category_type},
        )

    def delete_category(self) -> None:
        category_id = check_int_input("Enter category id: ")
        request_and_print(
            "DELETE", f"/categories/{category_id}", "Category deleted successfully"
        )
