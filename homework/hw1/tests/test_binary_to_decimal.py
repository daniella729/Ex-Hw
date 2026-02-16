from solution.binary_to_decimal import binary_to_decimal
<<<<<<< HEAD
import pytest


def test_binary_to_decimal():
    binary_number = "1101"
    assert binary_to_decimal(binary_number) == 13


def test_binary_to_decimal_zero():
    binary_number = "0"
    assert binary_to_decimal(binary_number) == 0


def test_binary_to_decimal_large():
    binary_number = "101010"
    assert binary_to_decimal(binary_number) == 42
=======
import pytest 
def test_binary_to_decimal():
    binary_number="1101"
    assert binary_to_decimal(binary_number)==13

def test_binary_to_decimal_zero():
    binary_number="0"
    assert binary_to_decimal(binary_number)==0

def test_binary_to_decimal_large():
    binary_number="101010"
    assert binary_to_decimal(binary_number)==42     









    
>>>>>>> 30bf1bb7f0770617d44cb7b49e66b0e201e3b5e9
