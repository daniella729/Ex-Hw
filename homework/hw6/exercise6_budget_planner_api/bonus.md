# Homework 6 - BONUS: Persistent Storage with Repository Pattern

## General Requirements

- The exercises must be submitted in your homework repository in a directory called `hw6` in a python package called `solution`.
- Each exercise should be implemented in a separate Python module with a given name.
- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Provide unit tests where asked using the `pytest` framework.
- Use parametrized tests where appropriate to cover multiple cases with less code.
- All the unit tests should be in a Python package called `tests`. Use a separate Python module for each exercise test suite.
- The unit test module should be called by convention `test_<subject>.py`
- Adhere to Python coding standards PEP-8
- Use Type Hints for function arguments and return values
- If the functions is long (beyond 15 lines of code), divide into more functions.
- Linting and Formatting Requirements - The Solution and the test code must be:
  - Formatted with `black` formatter before submission.
  - Pass `flake8` checks before submission.
  - Pass `mypy` type checks before submission.
- Navigate to the `linter-config` directory to find the `setup.cfg` file with the linters configuration. Copy all files to the root of your exercise directory to use the same configuration for your exercises.
- Remember to run flake8 from the root of your exercise directory to ensure it picks up the correct configuration, otherwise you will suffer from the cruelty of the default WPS rules.

---

## BONUS Exercise: Persistent Storage with Repository Pattern

### Description

This is an **optional bonus exercise** that extends Exercise 6 by adding persistent storage to your Budget Planner API. Instead of storing data in memory (which is lost when the application restarts), you'll implement a **repository layer** that persists data to JSON files.

This exercise focuses on:
- **Repository Pattern** - Separating data access logic from business logic
- **File I/O Operations** - Reading and writing JSON files
- **Dependency Injection** - Making your code more testable and maintainable
- **Abstraction** - Creating interfaces between layers

### Prerequisites

**CRITICAL**: Complete Exercise 6 (both Part 1 and Part 2) before attempting this bonus exercise. You should have a fully working Budget Planner API with a TUI that communicates via HTTP.

### Updated Directory Structure

After completing this bonus, your directory structure should look like:

```
hw6/
├── solution/
│   ├── __init__.py
│   ├── budget.py              # Business logic (can be called differently)
│   ├── budget_planner_api.py  # FastAPI application
│   ├── budget_planner_ui.py   # UI with HTTP requests
│   ├── ... your other python files and packages ...
│   └── repository/            # Repository package (This exercise)
│       ├── __init__.py
│       ├── file_accessor.py   # JSON file I/O operations
│       ├── income_repository.py    # Income repository
│       ├── expense_repository.py   # Expense repository
│       └── ... other repository files as needed ...
├── tests/
│   ├── __init__.py
│   ├── test_budget.py         # Tests for business logic (can be called differently)
│   ├── ... your other test files ...
│   └── test_repository/       # Repository tests package (This exercise)
│       ├── __init__.py
│       ├── test_file_accessor.py      # Tests for JsonFileAccessor
│       ├── test_income_repository.py  # Tests for IncomeRepository
│       ├── test_expense_repository.py # Tests for ExpenseRepository
│       └── ... other repository test files as needed ...
├── data/                      # Directory for JSON files (created at runtime)
├── venv/
├── .gitignore
├── setup.cfg
├── requirements.txt
└── README.md
```

---

## Requirements

### 1. JSON File Accessor Class

Create a class called `JsonFileAccessor` in a module named `repository/file_accessor.py` that encapsulates all file I/O operations for JSON files.

**Purpose**: This class provides a clean abstraction for reading and writing JSON data to files.

**Interface** (suggested methods):

```python
class JsonFileAccessor:
    """Handles reading and writing JSON data to files."""

    def __init__(self, file_path: str) -> None:
        """Initialize the accessor with a file path."""
        pass

    def read(self) -> dict:
        """Read data from the JSON file."""
        pass

    def write(self, data: dict) -> None:
        """Write data to the JSON file."""
        pass

    # Add other methods as needed (create_file, delete_file, etc.)
```

**Implementation Notes**:
- Use Python's `json` module for serialization/deserialization
- Handle file operations gracefully (check if file exists, create directories if needed)
- Handle errors appropriately (file not found, invalid JSON, etc.)

---

### 2. Repository Layer

Create repository classes in the `repository/` package. Each resource type should have its own repository module (e.g., `repository/income_repository.py`, `repository/expense_repository.py`).

**Purpose**: The repository layer abstracts data storage and retrieval operations from the business logic.

**Key Concepts**:
- Each resource type (e.g., Income, Expense, Category) should have its own repository class
- Repositories handle CRUD operations (Create, Read, Update, Delete)
- Repositories use `JsonFileAccessor` for file operations
- Each repository receives a `JsonFileAccessor` instance in its constructor

**Suggested Interface** (for each repository):

```python
class IncomeRepository:  # Or ExpenseRepository, CategoryRepository, etc.
    """Repository for managing income data persistence."""

    def __init__(self, file_accessor: JsonFileAccessor) -> None:
        """Initialize repository with a file accessor."""
        pass

    def create(self, item: Income) -> None:
        """Save a new item to storage."""
        pass

    def get(self, item_id: int) -> Income:
        """Retrieve an item by its ID."""
        pass

    def get_all(self) -> list[Income]:
        """Retrieve all items."""
        pass

    def update(self, item: Income) -> None:
        """Update an existing item."""
        pass

    def delete(self, item_id: int) -> None:
        """Delete an item by its ID."""
        pass
```

**Using Inheritance to Avoid Code Duplication**:

If you have multiple repositories with similar operations, consider creating a `BaseRepository` class that contains common CRUD logic. Specific repositories can inherit from it:

```python
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Base repository with common CRUD operations."""

    def __init__(self, file_accessor: JsonFileAccessor) -> None:
        self.file_accessor = file_accessor

    # Implement common methods here

class IncomeRepository(BaseRepository):
    """Specific repository for income."""

    # Override or add specific methods as needed
```

---

### 3. Integration with Business Logic

After implementing your repository classes:

1. **Update Business Logic**: Modify your business logic layer to use repository classes instead of storing data in memory
2. **Dependency Injection**: Pass repository instances to your business logic classes through their constructors. This will make your code more testable. It should be an optional parameter with a default value of `None` to maintain backward compatibility. If `None`, the business logic can create a repository instance it needs.

**Example**:
```python
# In repository/income_repository.py

from repository.file_accessor import JsonFileAccessor

DATA_FILE_PATH = "data/incomes.json"

class IncomeRepository:
    def __init__(self, file_accessor: JsonFileAccessor = None):
        self._file_accessor = file_accessor or JsonFileAccessor(DATA_FILE_PATH)

    # Implement CRUD methods using self._file_accessor
```

```python
# In budget.py (or your business logic module)

from repository.income_repository import IncomeRepository

class BudgetPlanner:
    def __init__(self, income_repository: IncomeRepository = None):
        self._income_repository = income_repository or IncomeRepository()

    # Use self._income_repository for all data operations
```

```python
# In budget_planner_api.py

from dataclasses import asdict
from budget import BudgetPlanner, Income

@app.post("/incomes/")
def create_income(income: dict):
    # Create an Income object from the input data
    income_obj = Income(**income)

    budget_planner = BudgetPlanner()
    new_income = budget_planner.create_income(income_obj)
    response_payload = asdict(new_income)
    return JsonResponse(content=response_payload, status_code=201)
```

---

## Testing Guidelines

### Test 1: JsonFileAccessor Tests

Write comprehensive tests for the `JsonFileAccessor` class in `tests/test_repository/test_file_accessor.py`.

**What to test**:
- Creating a new JSON file
- Reading data from a file
- Writing/updating data in a file
- Deleting a file
- Error handling (reading non-existent file, invalid JSON, etc.)

**Important**: These tests should perform **actual file I/O operations**. Use pytest's `tmp_path` fixture to create temporary test files that are automatically cleaned up:

```python
TEST_FILE_NAME = "test_data.json"
TEST_JSON_CONTENT = {"key": "value", "number": 42}

@pytest.fixture
def prepared_json_file(tmp_path):
    """Fixture to prepare a JSON file for testing."""
    file_path = tmp_path / TEST_FILE_NAME
    with open(file_path, "w") as f:
        json.dump(TEST_JSON_CONTENT, f)
    return file_path


def test_read(prepare_json_file):
    """Test reading and writing JSON data."""
    file_path = str(prepared_json_file)
    accessor = JsonFileAccessor(file_path)

    # Test your implementation
    content = accessor.read()
    assert content == TEST_JSON_CONTENT
```

---

### Test 2: Repository Tests with Mocks

Write tests for your repository classes in the `tests/test_repository/` package. Create separate test files for each repository (e.g., `test_income_repository.py`, `test_expense_repository.py`).

**CRITICAL**: Mock the `JsonFileAccessor` class in repository tests. Do NOT perform actual file I/O in these tests.

**Why mock?**
- Repository tests should focus on repository logic, not file operations
- Tests run faster without file I/O
- Tests are more reliable (no file system dependencies)

**How to mock**:
- Use `unittest.mock` to create mock objects
- Mock the `JsonFileAccessor` to simulate file operations

**What to test**:
- All CRUD operations (create, get, update, delete, get_all)
- Error handling (item not found, invalid data, etc.)
- Verify that the correct methods are called on the file accessor


## Tips

1. **Start with JsonFileAccessor**
   - Implement and test this class first
   - Make sure it handles all edge cases (missing files, invalid JSON, etc.)

2. **Use BaseRepository for Code Reuse**
   - If you have multiple repositories with similar logic, create a base class
   - Avoid duplicating code across repositories

3. **Test Thoroughly**
   - Write tests for JsonFileAccessor with actual file I/O
   - Write tests for repositories with mocked file accessors
   - Separate concerns: test file operations separately from repository logic

4. **Handle Errors Gracefully**
   - What happens if the JSON file is corrupted?
   - What happens if the data directory doesn't exist?
   - What happens if you try to get a non-existent item?

5. **Data Format**
   - Decide on a JSON structure for your data (e.g., list of dictionaries)
   - Consider how to handle IDs and uniqueness

6. **Backward Compatibility**
   - Your API endpoints shouldn't change
   - Your UI shouldn't need modifications
   - Only the internal data storage mechanism changes

---

## Architecture Overview

After completing this bonus, your architecture will include the repository and data access layers:

```
┌─────────────────────────────────────┐
│  UI Layer (budget_planner_ui.py)    │
│  - HTTP requests to API             │
└──────────────┬──────────────────────┘
               │ HTTP
               ▼
┌─────────────────────────────────────┐
│  API Layer (budget_planner_api.py)  │
│  - FastAPI routes                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Business Logic (budget.py)         │
│  - Business rules and calculations  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Repository Layer (repository.py)   │
│  - IncomeRepository                 │
│  - ExpenseRepository                │
│  - CRUD operations                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Data Access (file_accessor.py)     │
│  - JsonFileAccessor                 │
│  - File I/O operations              │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌────────────┐
        │ JSON Files │
        │ (data/)    │
        └────────────┘
```

---

## What You'll Learn

By completing this bonus exercise, you will gain practical experience with:

1. **Repository Pattern** - Abstracting data access logic
2. **File I/O Operations** - Reading and writing JSON files in Python
3. **Dependency Injection** - Passing dependencies through constructors
4. **Mocking in Tests** - Testing components in isolation
5. **Separation of Concerns** - Keeping layers independent
6. **Data Persistence** - Storing and retrieving data across application restarts
7. **Code Reuse** - Using inheritance to avoid duplication

---

## Documentation References

- **Python json module**: https://docs.python.org/3/library/json.html
- **Python pathlib**: https://docs.python.org/3/library/pathlib.html (for file path handling)
- **pytest fixtures**: https://docs.pytest.org/en/stable/fixture.html (especially `tmp_path`)
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html

---

Good luck with the bonus exercise! This is an excellent opportunity to practice important software engineering patterns. 🚀
