from functools import lru_cache

"""Return the n-th Fibonacci number using recursion with caching."""


@lru_cache(maxsize=None)
def fibonacci(number: int) -> int:
    first_value = 0
    second_value = 1
    if number < 1:
        raise ValueError("n must be greater than or equal to 1.")
    elif number == 1:
        return first_value
    elif number == 2:
        return second_value
    else:
        return fibonacci(number - 1) + fibonacci(number - 2)
