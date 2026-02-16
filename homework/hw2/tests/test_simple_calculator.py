import pytest

from soultion.simple_calculator import (
    INVALID_OPERATION,
    check_input,
    simple_calucaltor,
)


def test_check_input_invalid_length() -> None:
    assert check_input("add 1 2") == INVALID_OPERATION


def test_check_input_invalid_second_number() -> None:
    assert check_input("add 1 to b") == INVALID_OPERATION


def test_check_input_valid() -> None:
    result = check_input("add 1 to 2")
    assert result == ["add", "1", "to", "2"]


def test_add() -> None:
    assert simple_calucaltor("add 2 to 3") == "The answer is 5.0"


def test_subtract() -> None:
    assert simple_calucaltor("subtract 10 from 4") == "The answer is 6.0"


def test_multiply() -> None:
    assert simple_calucaltor("multiply 2 by 3") == "The answer is 6.0"


def test_divide() -> None:
    assert simple_calucaltor("divide 8 by 2") == "The answer is 4.0"


def test_divide_by_zero() -> None:
    assert simple_calucaltor("divide 5 by 0") == INVALID_OPERATION


def test_unknown_operation() -> None:
    assert simple_calucaltor("power 2 to 3") == INVALID_OPERATION


def test_invalid_format() -> None:
    assert simple_calucaltor("add 1 2") == INVALID_OPERATION
