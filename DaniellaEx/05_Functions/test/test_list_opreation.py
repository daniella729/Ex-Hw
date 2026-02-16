from soultion.list_opreation import filter_adults, get_names, sort_by_age
import pytest


def test_filter_adults_empty():
    people = []
    assert filter_adults(people) == people


def test_filter_is_adults():
    people = [
        {"name": "Alice", "age": 25},
        {"name": "Charlie", "age": 30},
        {"name": "Diana", "age": 18},
    ]
    assert filter_adults(people) == people


def test_filter_people_age():
    people = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 17},
        {"name": "Diana", "age": 16},
    ]
    assert filter_adults(people) == [{"name": "Alice", "age": 25}]


def test_get_name_empty():
    people = []
    assert get_names(people) == people


def test_get_name():
    people = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 17},
        {"name": "Charlie", "age": 30},
        {"name": "Diana", "age": 16},
    ]
    assert get_names(people) == ["Alice", "Bob", "Charlie", "Diana"]


def test_get_single_name():
    people = [{"name": "Bob", "age": 17}]
    assert get_names(people) == [{"name": "Bob", "age": 17}]


def test_sort_by_age_empty():
    people = []
    assert sort_by_age(people) == people


def test_sort_by_age():
    people = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 17},
        {"name": "Charlie", "age": 30},
        {"name": "Diana", "age": 16},
    ]
    assert sort_by_age(people) == [
        {"name": "Diana", "age": 16},
        {"name": "Bob", "age": 17},
        {"name": "Alice", "age": 25},
        {"name": "Charlie", "age": 30},
    ]


def test_sort_same_age():
    people = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 25}]
    assert sort_by_age(people) == people
