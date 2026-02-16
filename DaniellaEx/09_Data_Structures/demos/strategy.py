"""
DEMO - Usage of Dictionaries with callables as values to implement a strategy pattern.


## Optional Homework: Read about Strategy + Factory design patterns
"""


from typing import Callable
from art import tprint


def art_strategy(message: str) -> None:
    tprint(message)

def simple_strategy(message: str) -> None:
    print(f"SIMPLE: {message}")


STRATEGIES = {
    "ART": art_strategy
    "SIMPLE": simple_strategy
}


class Printer:

    def __init__(self, strategy: Callable[[str], None]):
        self.print_strategy = strategy

    def print(self, message: str) -> None:
        self.print_strategy(message)


def printer_factory(strategy_name: str) -> Printer:
    strategy = STRATEGIES.get(strategy_name)
    if strategy is None:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    return Printer(strategy)