from solution.extract_key_value import extract_key
import pytest


def test_check_key():
    key = "account"
    log_line = """2024-04-29 15:45:00,089 INFO 
    [name:starwars_engine.spaceship_manager.tasks]
    [pid:2995][uuid:20ebf460-dcdf-4b1f-abf1-7517ef3f63c2]
    [process:run_services_if_needed_wrapper]
    [function:run_services_if_needed]
    [account:519]
    [GamePlay:400004380] GamePlay's version is at least 'new' (5.2.0)."""
    assert extract_key(log_line, key) == "519"


def test_check_key2():
    key = "account"
    log_line = """2024-04-29 15:45:00,089 INFO 
    [name:starwars_engine.spaceship_manager.tasks]
    [pid:2995][uuid:20ebf460-dcdf-4b1f-abf1-7517ef3f63c2]
    [process:run_services_if_needed_wrapper]
    [function:run_services_if_needed]
    [account:51]
    [GamePlay:400004380] GamePlay's version is at least 'new' (5.2.0)."""
    assert extract_key(log_line, key) == "51"


def test_check_empty_key():
    key = "account1"
    log_line = """2024-04-29 15:45:00,089 INFO 
    [name:starwars_engine.spaceship_manager.tasks]
    [pid:2995][uuid:20ebf460-dcdf-4b1f-abf1-7517ef3f63c2]
    [process:run_services_if_needed_wrapper]
    [function:run_services_if_needed]
    [account1:]
    [GamePlay:400004380] GamePlay's version is at least 'new' (5.2.0)."""
    assert extract_key(log_line, key) == ""
