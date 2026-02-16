NAME = "name"
DEPARTMENTS = "departments"


def get_all_employee_names(company: dict) -> list[str]:
    """Return a flat list of all employee names in the company."""
    names: list[str] = []
    for department in company[DEPARTMENTS]:
        employees = get_department_employees(department)
        for employee in employees:
            names.append(employee[NAME])

    return names


def get_department_employees(department: dict) -> list[dict]:
    """Return a flat list of all employees in a single department."""
    employees: list[dict] = []
    for team in department["teams"]:
        for employee in team["employees"]:
            employees.append(employee)

    return employees


def get_employees_by_department(company: dict, department: str) -> list[str]:
    """Return employee names that belong to the given department name."""
    employees_by_department: list[str] = []
    for department1 in company[DEPARTMENTS]:
        if department1[NAME] == department:
            employees = get_department_employees(department1)
            for employee in employees:
                employees_by_department.append(employee[NAME])
    return employees_by_department


def get_average_salary_by_department(company: dict) -> dict[str, float]:
    """Return average salary per department."""
    salary_average: dict[str, float] = {}
    for department in company["departments"]:
        total_salary = 0
        count_salary = 0
        employees = get_department_employees(department)
        for employee in employees:
            total_salary += employee["salary"]
            count_salary += 1
        if count_salary > 0:
            average = round(total_salary / count_salary, 2)
        else:
            average = 0
        salary_average[department[NAME]] = average
    return salary_average


def get_high_earners(company: dict, threshold: int) -> dict[str, list[str]]:
    """Return {department_name: [employee_names]} for employees earning above threshold."""
    high_salary: dict[str, list[str]] = {}
    for department in company[DEPARTMENTS]:
        high_salary[department[NAME]] = []
        employees = get_department_employees(department)
        for employee in employees:
            if employee["salary"] > threshold:
                high_salary[department[NAME]].append(employee[NAME])
    return high_salary
