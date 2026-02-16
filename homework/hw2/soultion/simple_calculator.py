INVALID_OPERATION = "Invalid operation"


def print_calcualtor() -> None:
    print(
        """
          Simple Calcuator 
        --------------------
        Enter an operation in plain Engish.
        Type 'help' for examples.
        Type 'exit for quit.
        """
    )


def print_help() -> None:
    print(
        """ 
    How to use the calculator:
                
    Operations:      
        - add A to B 
        - subtract A from B 
        - multiply A by B 
        - divide A by B 
    """
    )


def check_input(operations: str) -> list[str] | str:
    """Validate the input format and return the split operation or INVALID_OPERATION."""
    split_operation = operations.split()
    if len(split_operation) != 4:
        return INVALID_OPERATION
    operation = split_operation[0]
    try:
        first_number = float(split_operation[1])
    except ValueError:
        return INVALID_OPERATION
    try:
        second_number = float(split_operation[3])
    except ValueError:
        return INVALID_OPERATION
    return split_operation


def simple_calucaltor(operations: str) -> str:
    """Perform a basic arithmetic operation based on user input."""
    list_operation = check_input(operations)
    operation = list_operation[0]
    if isinstance(list_operation, str):
        return list_operation
    first_number = float(list_operation[1])
    second_number = float(list_operation[3])
    if operation == "add":
        result = first_number + second_number

    elif operation == "subtract":
        result = first_number - second_number

    elif operation == "multiply":
        result = first_number * second_number

    elif operation == "divide":
        if second_number == 0:
            return INVALID_OPERATION
        else:
            result = first_number / second_number

    else:
        return INVALID_OPERATION
    return f"The answer is {result}"


def main() -> None:
    """Run the calculator loop and handle user commands."""
    print_calcualtor()
    while True:
        user_input = input("Enter operation:")
        user_input.lower()
        if user_input == "exit":
            print("Thank you for using our calcualtor")
            break
        elif user_input == "help":
            print_help()
            continue
        else:
            result = simple_calucaltor(user_input)
            print(result)


if __name__ == "__main__":
    main()
