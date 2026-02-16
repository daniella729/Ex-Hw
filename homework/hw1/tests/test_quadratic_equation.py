from solution.quadratic_equation import quadratic_equation
import pytest


def test_quadratic_equation():
    assert quadratic_equation(1, -5, 6) == "x1=3.00, x2=2.00"


def test_quadratic_equation_negative():
    assert quadratic_equation(1, 1, -6) == "x1=2.00, x2=-3.00"


def test_quadratic_equation_roots():
    assert quadratic_equation(3, -28, 48) == "x1=7.07, x2=2.26"
