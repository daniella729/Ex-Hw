from __future__ import annotations
from typing import Any
from functools import wraps
from typing import Callable



def check_args(args: list[Any], parameter_name: list[str], annotations: dict[str, Any])->None:
    """Validate positional arguments against the function's annotations."""
    index = 0
    while index < len(args) and index < len(parameter_name):
        name = parameter_name[index]
        value = args[index]
        expected = annotations.get(name)
        if expected is None:
            index += 1
            continue

        elif not isinstance(value, expected):
            raise TypeError(
                f"Argument '{name}' must be of type {expected}, "
                f"got {type(value)} instead."
            )
        index += 1


def check_kwargs(kwargs: dict[str, Any], annotations: dict[str, Any])->None:
    """Validate keyword arguments against the function's annotations."""
    for parameter_name, value in kwargs.items():
        expected = annotations.get(parameter_name)
        if expected is None:
            continue
        elif not isinstance(value, expected):
            raise TypeError(
                f"Argument '{parameter_name}' must be of type {expected}, "
                f"got {type(value)} instead."
            )


def checktype_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that enforces annotated argument and return types at runtime."""
    annotations = func.__annotations__
    parameter_names: list[str] = []
    for key in annotations:
        if key != "return":
            parameter_names.append(key)

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        check_args(list(args), parameter_names, annotations)
        check_kwargs(kwargs, annotations)
        result = func(*args, **kwargs)
        expected_return = annotations.get("return")
        if expected_return is not None:
            if not isinstance(result, expected_return):
                raise TypeError(
                    f"Return value must be {expected_return}, " f"got {type(result)}"
                )

        return result

    return wrapper
