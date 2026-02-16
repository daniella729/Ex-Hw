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
ALICE = "Alice"
BOB = "Bob"
CHARLIE = "Charlie"
DIANA = "Diana"
EVE = "Eve"

HIGH_THRESHOLD = 100000

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


def test_employee_names() -> None:
    company1 = company
    assert get_all_employee_names(company1) == [
        ALICE,
        BOB,
        CHARLIE,
        DIANA,
        EVE,
    ]


def test_employees_by_departmens() -> None:
    company2 = company
    assert get_employees_by_department(company2, ENGINEERING) == [
        ALICE,
        BOB,
        CHARLIE,
    ]
    company3 = company
    assert get_employees_by_department(company3, SALES) == [DIANA, EVE]


def test_by_average_salary() -> None:
    company4 = company
    assert get_average_salary_by_department(company4) == {
        ENGINEERING: 111666.67,
        SALES: 96500.0,
    }


def test_high_earners() -> None:
    company5 = company
    assert get_high_earners(company5, HIGH_THRESHOLD) == {
        ENGINEERING: [ALICE, BOB, CHARLIE],
        SALES: [],
    }
