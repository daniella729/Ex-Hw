# Homework 9: Budget Planner — SQLAlchemy & MySQL Persistence

## General Requirements

- The exercise must be submitted in your homework repository in a directory called `hw9`.
- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Provide unit tests where asked using the `pytest` framework.
- Advice: Write parameterized tests using the `@pytest.mark.parametrize` decorator.
- All the unit tests should be in a Python package called `tests`. Use a separate Python module for each test suite.
- The unit test module should be called by convention `test_<subject>.py`.
- Adhere to Python coding standards PEP-8.
- Use Type Hints for function arguments and return values.
- If a function is long (beyond 15 lines of code), divide it into smaller functions.
- Linting and Formatting Requirements — the solution and test code must be:
  - Formatted with `black` formatter before submission.
  - Pass `flake8` checks before submission.
  - Pass `mypy` type checks before submission.
- Use the attached `setup.cfg` for your linter configuration. Do not change it without permission.
- Run `flake8` from the root of your exercise directory.


---

## Exercise: Budget Planner — SQLAlchemy & MySQL Persistence

### Description

This exercise replaces the CSV-based persistence layer from Exercise 8 with a proper relational database, using **SQLAlchemy** as the ORM and **MySQL** as the database engine.

The business logic and all application behaviour remain **exactly the same** as in Exercise 8. Only the data persistence mechanism changes. You are swapping the storage backend — the application's features, API contracts, and UI are untouched.

### Prerequisites

**CRITICAL**: Complete Exercise 8 before starting this exercise. You must have a fully working Budget Planner with all four layers (UI, FastAPI (Routes), Service, Repository) implemented with CSV persistence.

Copy your `hw8/` directory to `hw9/` as your starting point.

---

## What Changes and What Stays the Same

### Must NOT change
- The TUI layer — any file under `solution/ui/`
- The FastAPI routers — any file under `solution/api/routers/`

### Must change
- The **Repository layer** — completely rewritten to use SQLAlchemy and MySQL instead of CSV files
- The **domain models** — Added SQLAlchemy ORM models, The existing data classes can act as interfaces between the service and the repository layers.
- The **Service layer** — minimal changes only (see below)
- `requirements.txt` — to add SQLAlchemy and related libraries. 

---

## Part 1 — Database Setup

- Create an EMPTY MySQL database called `budget_planner_ex9`. 
- Write the DB_NAME in an environment variable (e.g., in a `.env` file) so that your application can read it. DO NOT hardcode the database name or credentials in your code.

- See the example of a working FastAPI project in the our shared repo under: `modules/13_Databases/codevalue_school_full`. Do the same to connect your Budget planner app to MySQL using SQLAlchemy. 


### DB Model Alignment and Migrations

#### Option 1 — Alembic Migrations (Recommended)

- We didn't manage to cover Alembic migrations in the course yet. Still it is advised to use Alembic to manage your DB models.   
- See how Alembic is set up in the `codevalue_school_full` example and do the same in your project.

Commands you may need: 

```bash
# Create a new Alembic migration after defining your ORM models or Changing existing ones
alembic revision --autogenerate -m "Initial Migration"
```

```bash
# Apply all migrations
alembic upgrade head
```

- You may use GenAI to help you in everything related to Migrations and Alembic configuration.

**Linters and Formatters**: All Alembic related files, such as `env.py` or migration scripts should be IGNORED by linters and formatters. Please edit your `setup.cfg` to exclude these files from `flake8`, `black`, and `mypy` checks. 

#### Option 2 — Manual Schema Creation

- You can create the SQLAlchemy model first and then manually create the corresponding tables in MySQL using a MySQL client (e.g., MySQL Workbench) 
- You create and update a DB schema using the `CREATE TABLE` and `ALTER TABLE` SQL statements.

I think this option is more error-prone and less convenient than using Alembic, but it is still acceptable for this exercise if you are not comfortable with Alembic yet.

- You can use GenAI to help you write the SQL statements for creating and altering tables based on your SQLAlchemy models.

## Part 2 — ORM Models

Map each of your domain entities (Account, Category, etc ... ) to a **SQLAlchemy ORM model class**. Place these in a `solution/models/` package (you may have a separate module per entity).

Each ORM model must:
- Inherit from `Base`
- Define all columns with appropriate SQLAlchemy types (`String`, `Numeric`, `Date`, `Enum`, etc.)
- Define relationships and foreign key constraints as needed

## Part 3 — Repository Layer (Full Rewrite)

Completely rewrite the repository layer to use SQLAlchemy sessions instead of `CsvFileAccessor`.

**Important**: All repository methods should be `async`.

### Session Handling

Repositories do **not** create, commit, or roll back sessions. Instead, every repository method receives a `AsyncSession` as a parameter. The service layer is responsible for creating the session and committing or rolling it back via context managers. See the examples in `codevalue_school_full` for how to manage sessions in the service layer.

### BaseRepository

Rewrite `BaseRepository[T]` so that:
- Each CRUD method accepts a `AsyncSession` as its first parameter

### Concrete Repositories

Rewrite each concrete repository (AccountRepository, CategoryRepository, etc.) so that every method accepts a `AsyncSession` and uses it to execute queries. The rest of the public interface (method names, return types) should remain the same as in Exercise 8.

### Testing

We didn't cover testing with SQLAlchemy in the course yet, so there is no need to write unit tests for the repository layer in this exercise.

---

## Part 4 — Service Layer (Minimal Changes)

The service layer is now responsible for **session lifecycle management**. The rule is simple: **create a new session for every business operation, never reuse a session across different Business operations**.

The service receive an `async_session_maker` in the constructor 
- See example in `codevalue_school_full`: 
```
    def __init__(self, repo: Optional[StudentRepository] = None, session_maker=None):
        self.repo = repo or StudentRepository()
        self._session_maker = session_maker or async_session_maker
```     

For each service method:
1. Open a new session using `self._session_maker` as an async context manager
2. Pass the session to every repository method called within that operation
3. on Create/Update operations use the begin context manager to ensure that if any exception is raised, the transaction is rolled back automatically. 
```python
    async with self._session_maker() as session:
        async with session.begin():
            # Call repository methods with the same session
```
4. For read-only operations, you can just use `async with self._session_maker() as session:` without the `begin` context manager.

No business rules, validation logic, or calculated values (e.g., Net Worth, account balance) should change.

### Testing

Write Service unit tests that will test the business logic with mock session_maker and mock repositories. You can use `unittest.mock.AsyncMock` to create async mocks. 

- Provide the mock session_maker to the service constructor. Note that it must return an object that will mimic the behavior of an actual `async_session_maker`, meaning it should be an async context manager that yields a mock session object.
- The mock session itself should be able to return async context manager when using teh `begin` method.
- Recall what we learned in the course about Async Context Managers, and how to create one, then create the necessary infrastructure code that you will use in your tests. 
- Use Async mocks to mock your repository classes as well

---

## Suggested Directory Structure

```
hw9/
├── solution/
│   ├── __init__.py
│   ├── database.py                # Engine, async_session_maker, Base
│   ├── models/                    # SQLAlchemy ORM model classes
│   │   └── __init__.py
│   ├── repository/                # Layer 1: SQLAlchemy repositories
│   │   ├── __init__.py
│   │   ├── account_repository.py
│   │   ├── category_repository.py 
│   │   └── base_repository.py
│   ├── services/                  # Layer 2: business logic (minimal changes)
│   │   └── __init__.py
│   ├── api/                       # Layer 3: FastAPI (unchanged)
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routers/
│   │       └── __init__.py
│   └── ui/                        # Layer 4: TUI (unchanged)
│       └── __init__.py
├── tests/
│    __init__.py
│   └── test_service/
│       └── __init__.py
│   └── conftest.py                # fixtures for mock session_maker and mock repositories
├── .env                           # DB connection params
├── .env_sample                    # Example .env
├── venv/
├── setup.cfg
├── requirements.txt
├── lint.sh                        # Or lint.ps1 for Windows
├── .gitignore
└── README.md
```

> Add `.env` to your `.gitignore`. Never commit database credentials.

---

## What You'll Learn

By completing this exercise you will gain practical experience with:

1. **SQLAlchemy ORM** — defining models, relationships, and querying with the ORM
2. **Async SQLAlchemy** — using  `AsyncSession`, and `async_session_maker` with the `aiomysql` driver
3. **Session lifecycle management**
4. **Swapping persistence backends** — replacing one storage implementation with another without changing business logic
5. **Environment-based configuration** — managing database credentials securely
6. **Testing with async mocks** — writing unit tests for service layer with mocked async sessions and repositories
7. **Database Migrations** — using Alembic to manage schema changes (if you choose that option)

---

Good luck! 💰
