from soultion.type_checking_function import checktype_decorator
from typing import Any
import pytest
KEY ="key"

@checktype_decorator
def format_data(name: str, age: int, data: dict, other_info:object | None = None) -> str:
    other_info_str = f", Other Info : {other_info}" if other_info else ""
    return f"Name: {name}, Age: {age}, Data: {data[KEY]}{other_info_str}"


@checktype_decorator
def bad_return(name: str) -> str:
    return 123  # type: ignore[return-value] 



def test_format_data_args_only() -> None:
    result = format_data("Alice", 30, {KEY: "value"}, 1234)
    assert result == "Name: Alice, Age: 30, Data: value, Other Info : 1234"


def test_format_data_kwargs_only() -> None:
    result = format_data(
        name="Carol", age=22, data={KEY: "kwarg_test"}, other_info=None
    )
    assert result == "Name: Carol, Age: 22, Data: kwarg_test"


def test_format_data_other_info_various_types() -> None:
    result_str = format_data("Dave", age=40, data={KEY: "abc"}, other_info="extra")
    assert result_str == "Name: Dave, Age: 40, Data: abc, Other Info : extra"


def test_format_data_uncorrect_values() -> None:
    with pytest.raises(TypeError):
        format_data("Frank", "28", {KEY: 100})


def test_check_return_type() -> None:
    with pytest.raises(TypeError):
        bad_return("Frank")
