from solution.ui.api_client import request_and_print, request_json
from solution.ui.input_check import (
    check_decimal_input,
    check_input,
    check_int_input,
    check_choice_input,
)


class AccountUI:
    """CLI UI that communicates with the Account Planner API server."""

    def __init__(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Account Menu =====")
        print("1. View all accounts")
        print("2. Add account")
        print("3. Edit account name")
        print("4. Delete account")
        print("5. View account balance")
        print("6. view net worth")
        print("7. Back\n")

    def handle_choice(self) -> None:
        choice = check_choice_input(
            "Choose an option: ",
            {"1", "2", "3", "4", "5", "6", "7"},
        )

        if choice == "7":
            self.running = False

        match choice:
            case "1":
                self.view_all_accounts()
            case "2":
                self.add_account()
            case "3":
                self.edit_account_name()
            case "4":
                self.delete_account()
            case "5":
                self.view_account_balance()
            case "6":
                self.view_net_worth()

    def view_all_accounts(self) -> None:
        accounts = request_json("GET", "/accounts")
        if accounts is None:
            return
        if not accounts:
            print("No accounts found")
        for account in accounts:
            print(account)

    def add_account(self) -> None:
        name = check_input("Enter account name: ")
        opening_balance = check_decimal_input("Enter opening balance:")
        currency = check_input("Enter ILS currency:")
        if currency != "ILS":
            print("Only ILS currency is supported")
            return
        request_and_print(
            "POST",
            "/accounts",
            "Account created successfully",
            {
                "name": name,
                "opening_balance": str(opening_balance),
                "currency_just_ILS": currency,
            },
        )

    def edit_account_name(self) -> None:
        account_id = check_int_input("Enter account id: ")
        new_name = check_input("Enter new account name:")
        request_and_print(
            "PATCH",
            f"/accounts/{account_id}",
            "Account updated successfully",
            {"new_name": new_name},
        )
       
    def delete_account(self) -> None:
        account_id = check_int_input("Enter account id: ")
        request_and_print(
            "DELETE", f"/accounts/{account_id}", "Account deleted successfully"
        )

    def view_account_balance(self) -> None:
        account_id = check_int_input("Enter account id: ")
        account_details = request_json("GET", f"/accounts/{account_id}/balance")
        if account_details is not None:
            print(account_details)

    def view_net_worth(self) -> None:
        net_worth = request_json("GET", "/accounts/net-worth")
        if net_worth is not None:
            print(net_worth)
