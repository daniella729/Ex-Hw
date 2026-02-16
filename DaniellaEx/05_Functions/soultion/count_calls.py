from typing import Callable
from functools import wraps


def count_call_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count = wrapper.call_count + 1
        result = func(*args, **kwargs)

    wrapper.call_count = 0
    return wrapper


@count_call_decorator
def greet(name: str) -> str:
    return f"Hello, {name}!"
