import sys


def variable_type_size() -> None:
    """Print the type, value, and memory size of different variables using sys.getsizeof"""
    print(f"Type: {type(1)}, value: {1} size: {sys.getsizeof(1)}")
    print(f"Type: {type(3.14)}, value: {3.14} size: {sys.getsizeof(3.14)}")
    print(f"Type: {type('hello')}, value: {'hello'} size: {sys.getsizeof('hello')}")
    print(f"Type: {type(-1)}, value: {-1} size: {sys.getsizeof(-1)}")
    print(f"Type: {type('x' * 10)}, value: {'x' * 10} size: {sys.getsizeof('x' * 00)}")


variable_type_size()
