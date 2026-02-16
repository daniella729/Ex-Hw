from soultion.count_calls import count_call_decorator
import pytest


def test_call_count_none():
    @count_call_decorator
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    assert greet.call_count == 0


def test_call_count1():
    @count_call_decorator
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    greet("Alice")
    assert greet.call_count == 1


def test_call_count2():
    @count_call_decorator
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    greet("Alice")
    greet("Bob")
    assert greet.call_count == 2


def test_call_count3():
    @count_call_decorator
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    greet("Alice")
    greet("Bob")
    greet("Bob")
    assert greet.call_count == 3
