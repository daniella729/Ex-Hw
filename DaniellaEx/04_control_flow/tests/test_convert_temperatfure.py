from soultion.convert_temperature import convert_temperature, validate_temperature
import pytest


def test_validation_from_unit():
    with pytest.raises(ValueError):
        convert_temperature(10, "X", "C")


def test_validation_to_unit():
    with pytest.raises(ValueError):
        convert_temperature(10, "C", "x")


def test_kelvin_negative_value():
    with pytest.raises(ValueError):
        convert_temperature(-1, "K", "C")


def test_celsius_below_absolute_zero():
    with pytest.raises(ValueError):
        convert_temperature(-300, "C", "K")


# test for conver temperature
def test_same_unit():
    assert convert_temperature(14, "K", "K") == 14


def test_c_to_f():
    assert convert_temperature(0, "C", "F") == 32.0


def test_c_to_k():
    assert convert_temperature(100, "C", "K") == 373.15


def test_f_to_k():
    assert convert_temperature(32, "F", "C") == 0


def test_k_to_c():
    assert convert_temperature(273.15, "K", "C") == 0
