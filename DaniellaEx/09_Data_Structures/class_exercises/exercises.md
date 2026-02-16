# Class Exercises: Data Structures

## General Requirements

- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Provide unit tests where asked using the `pytest` framework.
- All the unit tests should be in a Python package called `tests`. Use a separate Python module for each exercise test suite.
- The unit test module should be called by convention `test_<subject>.py`
- Adhere to Python coding standards PEP-8
- Use Type Hints for function arguments and return values
- If the functions is long (beyond 15 lines of code), divide into more functions.
- Linting and Formatting Requirements - The Solution and the test code must be:
  - Formatted with `black` formatter before submission.
  - Pass `flake8` checks before submission. Use `wps explain <error code>` to understand the error and how to write correctly.
  - Pass `mypy` type checks before submission.
- Navigate to the `linter-config` directory to find the `setup.cfg` file with the linters configuration. Copy all files to the root of your exercise directory to use the same configuration for your exercises.

---


## Exercise 2: Nested Data Structure Analysis with Comprehensions

**Description:**
Work with nested data structures representing a company's organizational data. Use list and dictionary comprehensions to extract and transform information efficiently.

**Requirements:**
- Given a nested structure of departments, teams, and employees (see example below)
- Implement `get_all_employee_names(company: dict) -> list[str]` - returns a flat list of all employee names using list comprehension
- Implement `get_employees_by_department(company: dict, department: str) -> list[str]` - returns employee names for a specific department using list comprehension
- Implement `get_average_salary_by_department(company: dict) -> dict[str, float]` - returns a dictionary with department names as keys and average salaries as values using dict comprehension
- Implement `get_high_earners(company: dict, threshold: int) -> dict[str, list[str]]` - returns a nested dictionary where keys are department names and values are lists of employee names earning above the threshold, using nested comprehensions
- Include type hints for all functions
- Write at least 3 unit tests for each function

**Example:**

```python
company = {
    "departments": [
        {
            "name": "Engineering",
            "teams": [
                {
                    "name": "Backend",
                    "employees": [
                        {"name": "Alice", "salary": 120000},
                        {"name": "Bob", "salary": 110000}
                    ]
                },
                {
                    "name": "Frontend",
                    "employees": [
                        {"name": "Charlie", "salary": 105000}
                    ]
                }
            ]
        },
        {
            "name": "Sales",
            "teams": [
                {
                    "name": "Direct Sales",
                    "employees": [
                        {"name": "Diana", "salary": 95000},
                        {"name": "Eve", "salary": 98000}
                    ]
                }
            ]
        }
    ]
}

# Get all employee names
names = get_all_employee_names(company)
# Output: ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']

# Get average salary by department
avg_salaries = get_average_salary_by_department(company)
# Output: {'Engineering': 111666.67, 'Sales': 96500.0}

# Get high earners above 100000
high_earners = get_high_earners(company, 100000)
# Output: {'Engineering': ['Alice', 'Bob', 'Charlie'], 'Sales': []}
