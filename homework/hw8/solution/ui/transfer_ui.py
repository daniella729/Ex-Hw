from solution.ui.api_client import request_and_print, request_json
from solution.ui.input_check import (
    check_decimal_input,
    check_input,
    check_int_input,
    check_choice_input,
    check_date_input,
)


class TransferUI:
    """CLI UI that communicates with the transferr Planner API server."""

    def __init__(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            self.print_menu()
            self.handle_choice()

    def print_menu(self) -> None:
        print("\n===== Transfers Menu =====")
        print("1. View all transfers")
        print("2. Add transfer")
        print("3. Delete transfer")
        print("4. Back\n")

    def handle_choice(self) -> None:
        choice = check_choice_input(
            "Choose an option: ",
            {"1", "2", "3", "4"},
        )
        match choice:
            case "1":
                self.view_all_transfers()
            case "2":
                self.add_transfer()
            case "3":
                self.delete_transfer()
            case "4":
                self.running = False

    def view_all_transfers(self) -> None:
        all_transfers = request_json("GET", "/transfers")
        if all_transfers is None:
            return
        if not all_transfers:
            print("No transfer found")
        for transfer in all_transfers:
          print(transfer)    
        
    def add_transfer(self) -> None:
        description = check_input("Enter description: ")
        amount = check_decimal_input("Enter amount: ")
        transfer_date = check_date_input("Enter transfer date (YYYY-MM-DD): ")
        from_account_id = check_int_input("Enter from account id: ")
        to_account_id = check_int_input("Enter to account id: ")
        request_and_print(
            "POST",
            "/transfers",
            "Transfer created successfullu",
            {
                "description": description,
                "amount": amount,
                "transfer_date": transfer_date,
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
            },
        )
        

    def delete_transfer(self) -> None:
        transfer_id = check_int_input("Enter transfer id: ")
        request_and_print(
            "DELETE",
            f"/transfers/{transfer_id}",
            "transfer deleted successfully",
        )
