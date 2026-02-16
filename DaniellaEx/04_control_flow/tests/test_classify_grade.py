from soultion.classify_grade import classify_grade
import pytest


def test_valide_range():
    with pytest.raises(ValueError):
        classify_grade(-1)
    with pytest.raises(ValueError):
        classify_grade(101)


def test_score_checka():
    assert classify_grade(98) == "A"


def test_score_checkb():
    assert classify_grade(85) == "B"


def test_score_checkc():
    assert classify_grade(71) == "C"


def test_score_checkd():
    assert classify_grade(62) == "D"


def test_score_checkf():
    assert classify_grade(55) == "F"
