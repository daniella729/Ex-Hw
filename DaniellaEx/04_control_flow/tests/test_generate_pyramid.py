from soultion.generate_pyramid import generate_pyramid, validation_generate_pyramid
import pytest


def test_hight_1():
    result = "1"
    assert generate_pyramid(1) == result


def test_hight_2():
    result = """ 1
121"""
    assert generate_pyramid(2) == result


def test_hight_3():
    result = """  1
 121
12321"""
    assert generate_pyramid(3) == result


def test_hight_4():
    result = """   1
  121
 12321
1234321"""
    assert generate_pyramid(4) == result


def test_valide_generate_pyramid():
    with pytest.raises(ValueError):
        generate_pyramid(-1)
    with pytest.raises(ValueError):
        generate_pyramid(10)
