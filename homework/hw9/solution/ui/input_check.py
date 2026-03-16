from decimal import Decimal, InvalidOperation
from datetime import datetime


def check_input(user_input: str) -> str:
    while True:
        value = input(user_input)
        if value == "":
            print("Value cannot be empty.")
            continue
        return value


def check_int_input(user_input: str) -> int:
    while True:
        value = input(user_input)
        try:
            return int(value)
        except ValueError:
            print("please enter a valid integer")


def check_decimal_input(user_input: str) -> Decimal:
    while True:
        value = input(user_input)
        try:
            return Decimal(value)
        except InvalidOperation:
            print("please enter a valid number")


def check_date_input(user_input: str) -> str:
    while True:
        value = input(user_input).strip()
        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d")
            if parsed_date.strftime("%Y-%m-%d") == value:
                return value
        except ValueError:
            ...
        print("Please enter a date in YYYY-MM-DD format")


def check_choice_input(user_input: str, allowed_values: set[str]) -> str:
    while True:
        value = input(user_input).strip()
        if value in allowed_values:
            return value
        choices = ",".join(sorted(allowed_values))
        print("please choose one of :", choices)
