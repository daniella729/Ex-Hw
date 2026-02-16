from solution.extract_data import extract_data_from_html
import pytest


def test_string_multiple_titles1():
    html_line = (
        "<html><head><title>My Title</title>second title </head><body></body></html>"
    )
    assert extract_data_from_html(html_line) == "My Title"


def test_string_multiple_titles2():
    html_line = "<html><head><title>My Title2</title></head><body></body></html>"
    assert extract_data_from_html(html_line) == "My Title2"


def test_string_one_title():
    html_line = "<html><head><title>My Title</title></head><body></body></html>"
    assert extract_data_from_html(html_line) == "My Title"
