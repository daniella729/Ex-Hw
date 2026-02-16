from soultion.fibonacci import fibonacci
import pytest


def test_check_fibonacci_value() -> None:
    fibonacci.cache_clear
    assert fibonacci(10) == 34
    fibonacci.cache_clear
    assert fibonacci(150) == 6161314747715278029583501626149
    fibonacci.cache_clear()
    assert fibonacci(200) == 173402521172797813159685037284371942044301
    fibonacci.cache_clear()
    assert fibonacci(1) == 0
    fibonacci.cache_clear()
    assert fibonacci(2) == 1
    fibonacci.cache_clear()
    assert fibonacci(3) == 1


def test_check_fibonacci_value_less_than_one() -> None:
    with pytest.raises(ValueError):
        fibonacci(-1)
