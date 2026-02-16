from typing import Any

from soultion.data_structure import (
    get_all_employee_names,
    get_average_salary_by_department,
    get_employees_by_department,
    get_high_earners,
)

DEPARTMENTS = "departments"
TEAMS = "teams"
EMPLOYEES = "employees"
NAME = "name"
SALARY = "salary"

ENGINEERING = "Engineering"
SALES = "Sales"
OPERATIONS = "Operations"

ALICE = "Alice"
BOB = "Bob"
CHARLIE = "Charlie"
DIANA = "Diana"
EVE = "Eve"
SARA = "Sara"

company = {
    DEPARTMENTS: [
        {
            NAME: ENGINEERING,
            TEAMS: [
                {
                    NAME: "Backend",
                    EMPLOYEES: [
                        {NAME: ALICE, SALARY: 120000},
                        {NAME: BOB, SALARY: 110000},
                    ],
                },
                {
                    NAME: "Frontend",
                    EMPLOYEES: [{NAME: CHARLIE, SALARY: 105000}],
                },
            ],
        },
        {
            NAME: SALES,
            TEAMS: [
                {
                    NAME: "Direct Sales",
                    EMPLOYEES: [
                        {NAME: DIANA, SALARY: 95000},
                        {NAME: EVE, SALARY: 98000},
                    ],
                }
            ],
        },
    ]
}

another_company = {
    DEPARTMENTS: [
        {
            NAME: OPERATIONS,
            TEAMS: [
                {
                    NAME: "Recruitment_Team",
                    EMPLOYEES: [{NAME: SARA, SALARY: 50000}],
                }
            ],
        }
    ]
}

HIGH_THRESHOLD = 200000
LOW_THRESHOLD = 0


def test_employee_names_empty_company() -> None:
    empty_company: dict[str, Any] = {DEPARTMENTS: []}
    assert get_all_employee_names(empty_company) == []


def test_employee_names_single_department() -> None:
    company = another_company
    assert get_all_employee_names(company) == [SARA]


def test_employees_by_department_not_found() -> None:
    assert get_employees_by_department(company, OPERATIONS) == []


def test_employees_by_department_empty_department() -> None:
    company = {
        DEPARTMENTS: [
            {NAME: OPERATIONS, TEAMS: []},
        ]
    }
    assert get_employees_by_department(company, OPERATIONS) == []


def test_average_salary_empty_company() -> None:
    empty_company: dict[str, Any] = {DEPARTMENTS: []}
    assert get_average_salary_by_department(empty_company) == {}


def test_average_salary_single_employee() -> None:
    company = another_company
    assert get_average_salary_by_department(company) == {OPERATIONS: 50000.0}


def test_high_earners_high_threshold() -> None:
    assert get_high_earners(company, HIGH_THRESHOLD) == {
        ENGINEERING: [],
        SALES: [],
    }


def test_high_earners_low_threshold() -> None:
    assert get_high_earners(company, LOW_THRESHOLD) == {
        ENGINEERING: [ALICE, BOB, CHARLIE],
        SALES: [DIANA, EVE],
    }
