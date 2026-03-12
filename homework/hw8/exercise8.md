# Homework 8: Budget Planner — Accounts, Persistence & Data Portability

## General Requirements

- The exercise must be submitted in your homework repository in a directory called `hw8`.
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

**Note**: In this exercise you will have more operations to support. Think how to divide them into menus and submenus in the UI, Read about FastAPI routers, design your classes to be focused and not have too many methods. 
The attached `setup.cfg` has some relaxed limits on the number of methods and module members, but try to keep your classes focused and not have too many methods.

---

## Exercise: Budget Planner — Accounts, Persistence & Data Portability

### Description

This exercise significantly expands the **Budget Planner** you built in Exercise 4 and Exercise 6. You will add meaningful new features to the application domain, redesign the architecture to support **real data persistence using CSV files**, and connect all the layers through a **FastAPI REST API**.

The exercise has three parts plus an optional bonus:

- **Part 1** — Extend the domain with new features and design your data models.
- **Part 2** — Implement the full 4-layer application architecture.
- **Part 3** — Design the equivalent relational database schema and write the SQL queries the application would use.
- **Bonus** — Replace the text-based TUI with a rich terminal UI using the Textual library.

### Prerequisites

**CRITICAL**: Complete Exercise 4 (Budget Planner CLI) and Exercise 6 (Budget Planner REST API) before starting this exercise.

You will build directly on top of your EX6 codebase. **Copy your `hw6/` directory to `hw8/` as your starting point.** Be warned: the new features and the new architecture require significant refactoring/re-design of your existing code. This is intentional — refactoring is a core skill.

---

## Part 1 — New Features & Data Design

### 1.1 New Features

Your Budget Planner must be extended with the following features. Read through all of them carefully before writing any code — they are interconnected, and understanding the full picture will help you design your data models correctly.

#### Categories

Every income and expense transaction must belong to a **category**. A category has a name and a type — either an income category or an expense category. You should pre-seed a few default categories when the application starts with an empty database (e.g., `Salary`, `Freelance`, `Rent`, `Groceries`, `Utilities`, `Entertainment`), but users must also be able to add and remove their own.

#### Dates on Transactions

Every transaction must record the **date** it occurred. This enables the application to filter transactions by month, show monthly summaries, and display spending trends over time.

#### Multiple Accounts

Instead of a single global pool of money, users can now manage **multiple accounts**. Think of it like having several bank accounts — a main checking account, a savings account, a cash wallet, a credit card. Each account has a **name** and an **opening balance** (the balance at the time the account was added to the app).

Every income and expense transaction is associated with a specific account.

> **Important:** Account balances can be **negative**. A credit card account starts at 0 and goes negative as you spend on it (it represents money you owe). An overdrawn bank account also has a negative balance. Your application must handle this correctly.

#### Transfers Between Accounts

Users must be able to **transfer money from one account to another**. For example: "transfer $2,000 from my checking account to savings" or "transfer $500 from my credit card balance to checking".

#### Net Worth

The application must be able to show the user their **Net Worth**.

> **What is Net Worth?**
> Net Worth is the total value of everything you own minus everything you owe, expressed as a single number. In the context of this application: **Net Worth = the sum of the current balances of all your accounts**.
>
> Since account balances can be negative (e.g., a credit card you owe money on), Net Worth naturally accounts for liabilities. If your checking account has $5,000, your savings has $10,000, and your credit card balance is −$2,000, your Net Worth is $13,000.
>
> Net Worth is a **calculated, read-only value** — it is never stored. It is always derived from the current state of all account balances.

#### Import / Export (Data Portability)

The application must support exporting all data to a `.zip` file and importing it back.

- **Export**: Package all CSV data files into a single `.zip` archive. The user saves this file for backup or to migrate to a different machine.
- **Import**: Receive a `.zip` file, extract and validate its contents, and rebuild the entire application database from it.
  - **Validation** must check: all required CSV files are present, all required columns exist in each file, data types are correct, and referential integrity is intact (e.g., every transaction references a valid account and a valid category).
  - If validation **fails**: reject the import with a clear error message. The existing data must not be modified.
  - If validation **passes**: replace all existing data with the imported data.

- You are expected to search the web and figure out how to work with zip files in Python.

---

### 1.2 Required Operations

The following is the complete list of operations the Budget Planner must support. Every layer of the application — the TUI, the API, the service layer, and the repository layer — must be designed to support all of these. This list also defines the scope of the SQL queries in Part 3.

**Accounts**
1. View all accounts with their current balance
2. Add a new account
3. Edit an account's name
4. Delete an account
5. View the current balance of a single account
6. View Net Worth (total balance across all accounts)

**Categories**
7. View all categories
8. Add a new category
9. Delete a category

**Transactions**
10. View all transactions, with optional filtering by account and by month/year
11. Add an income transaction
12. Add an expense transaction
13. Delete a transaction

**Transfers**
14. View all transfers
15. Add a transfer between two accounts
16. Delete a transfer

**Summaries & Reports**
18. View spending breakdown by category for a given month



---

### 1.3 Data Design

Before writing any code, take time to design your data models on paper.

Think about:
- What are the **entities** in this application? What data does each one hold?
- What are the **relationships** between entities? Which entities reference others?
- Which values are **stored** and which are **derived/calculated** (and therefore never stored)?
- What Python types are appropriate for each field? Consider using `Decimal` for money (not `float` — floating point precision errors are unacceptable in financial applications), `date` for dates, and `Enum` for fixed sets of values.

You will represent your entities as Python **dataclasses**. You should also think about your data model in parallel with the SQL design in Part 3, because your CSV files will mirror your database tables exactly — each CSV file corresponds to one table, with the same columns.

---

## Part 2 — Application Architecture

### Overview

Your application must follow a strict **4-layer architecture**. Each layer has a single responsibility and communicates only with the layer directly below it.

```
┌──────────────────────────────────────────────────────┐
│  Layer 4 — TUI  (text-based  OR  Textual — BONUS)    │
└───────────────────────────┬──────────────────────────┘
                            │  HTTP requests
                            │  (requests library)
                            ▼
┌──────────────────────────────────────────────────────┐
│  Layer 3 — FastAPI                                   │
│  /accounts  /categories /net-worth  /summary ...     │
└───────────────────────────┬──────────────────────────┘
                            │  function calls
                            ▼
┌──────────────────────────────────────────────────────┐
│  Layer 2 — Service Layer                             │
│  Business logic, domain rules, orchestrates repos    │
└───────────────────────────┬──────────────────────────┘
                            │  function calls
                            ▼
┌──────────────────────────────────────────────────────┐
│  Layer 1 — Repository Layer                          │
│  Work with CsvFileAccessor to read/write CSV files   │
└───────────────────────────┬──────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  CSV Files  (data/)     │
              │  (one file per entity)  │
              └─────────────────────────┘
```

Build each layer from the bottom up: Repository → Service → FastAPI → TUI.

---

### Layer 1 — Repository Layer

The repository layer is responsible for **all CSV file I/O**. No business logic belongs here.

#### Why CSV?

CSV (Comma-Separated Values) is a row-oriented format perfectly suited to tabular financial data. It is widely used for data export in banking and accounting tools. In this exercise, each CSV file represents one entity table — its columns map directly to the columns of the corresponding database table you will design in Part 3.

#### CsvFileAccessor

Create a low-level class called `CsvFileAccessor` that wraps all file operations for a single CSV file. It should handle:
- Reading all rows from the file as a list of dictionaries.
- Writing a full list of dictionaries back to the file (overwriting it).
- Edge cases: file does not exist, file is empty, missing header row.

The file path must be given in the constructor. This class knows nothing about domain entities — it only speaks in plain `dict` rows.

If you wish, you can work with any library for CSV handling,

#### BaseRepository

Create a generic base class `BaseRepository[T]` that provides standard CRUD operations for any entity type `T`:

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def create(self, item: T) -> T: ...
    def get(self, item_id: int) -> T: ...
    def get_all(self) -> list[T]: ...
    def update(self, item: T) -> T: ...
    def delete(self, item_id: int) -> None: ...
```

Recommended Design: **one repository class per entity**. You decide how many entities you have and what their repositories look like based on your data design from Part 1.

#### Testing

- `CsvFileAccessor` tests: use pytest's `tmp_path` fixture to perform real file I/O in a temporary directory.
- Repository tests: **mock** the `CsvFileAccessor` — do not perform real file I/O in these tests. Use `unittest.mock` to verify repository logic in isolation.

---

### Layer 2 — Service Layer

The service layer contains all **business logic and domain rules**. Services orchestrate one or more repositories to fulfil a use case. This layer has no knowledge of HTTP, CSV files, or the TUI.

Think carefully about which services you need. Consider:
- Which operations involve calculations (not just simple CRUD)?
- Which operations touch more than one entity (e.g., creating a transfer involves two accounts)?
- Which domain rules must be enforced (e.g., a transfer's source and destination cannot be the same account)?
- Which features require orchestrating multiple repositories at once (e.g., import/export)?

> **Reminder**: Account balance and Net Worth are **calculated values**. They must never be stored — always compute them on demand from the live data.

#### Testing

Service tests must **mock all repositories**. The service layer should be fully testable without any file system involvement.

---

### Layer 3 — FastAPI Layer

The FastAPI layer exposes the service layer as a **REST API**. Routes receive HTTP requests, call the appropriate service method, and return responses. No business logic and no CSV file operations belong here.

#### Organise with Routers

Your API will have many endpoints. Read the FastAPI documentation on [Bigger Applications — Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/) and use `APIRouter` to split your endpoints into separate modules by resource (e.g., one router for accounts, one for transactions, one for transfers). Attach all routers to the main FastAPI application.

#### API Endpoints example

**Accounts**
- `GET /accounts` — list all accounts with their current balance
- `POST /accounts` — create a new account
- `PUT /accounts/{id}` — update an account name
- `DELETE /accounts/{id}` — delete an account

**Net Worth**
- `GET /net-worth` — get the total Net Worth across all accounts

**Categories**
- `GET /categories` — list all categories
 ... 

> **New FastAPI skills for this part:**
> - `FileResponse` — to return a file as an HTTP response for the export endpoint.
> - `UploadFile` — to receive a file upload in a request body for the import endpoint.
> Read the FastAPI documentation on [Request Files](https://fastapi.tiangolo.com/tutorial/request-files/).

#### No Tests Required for FastAPI

You are not required to write automated tests for the FastAPI layer. Test your endpoints manually using Swagger UI (`http://localhost:8000/docs`) or curl.

---

### Layer 4 — TUI Layer

The TUI (Text User Interface) is the user-facing client. It communicates with the application **exclusively via HTTP requests** to the FastAPI layer — exactly as in Exercise 6 Part 2. It must have **no direct imports** from the service or repository layers.

The design and implementation of the TUI is **entirely up to you**. You may use a simple text-based menu with `input()` and `print()` (as in EX4), or a richer interface. The only requirements are:

1. The TUI must support all required operations
2. All communication must go through HTTP.
3. HTTP errors must be handled gracefully — including the API being unreachable.
4. For **export**: prompt the user for a save path, call `GET /export`, and write the response bytes to disk.
5. For **import**: prompt the user for a zip file path, read the file, and send it as a multipart upload to `POST /import`. Display the validation result.
6. Before importing, display a **clear warning** to the user: importing will replace all existing data.

---

## Part 3 — SQL Database Design

The same Budget Planner application you are building in Part 2 could be backed by a relational database instead of CSV files. In this part you will design that database, populate it, and write the SQL queries that the application would execute.

> This part is independent of the Python implementation — you do not need to connect MySQL to your Python code. The purpose is to practice SQL and to understand how your data design translates to a relational schema.
>
> Notice that the tables you create here should mirror the structure of the CSV files you designed in Part 2. This is intentional — the CSV files act as a flat-file database, and a real database is the natural next step.

### Sub-Part A — Entity Design (Pen & Paper)

Before writing any SQL, design your schema on paper.

Given the business requirements you implemented:
- Accounts with a name and opening balance
- Transactions (income and expense) linked to an account and a category, with a date
- Transfers that move money between two accounts
- Categories with a type (income or expense)

Tasks:
1. Identify all entities (tables) and their columns with appropriate SQL data types.
2. Identify all relationships between entities. Which are one-to-many? Decide where to place foreign keys.
3. Draw an ERD (Entity Relationship Diagram).

### Sub-Part B — Create the Schema

Create a database called `budget_planner` in MySQL. Implement all tables with:
- Appropriate column types (`VARCHAR`, `DECIMAL`, `DATE`, `ENUM`, `BOOLEAN`, etc.)
- Primary keys with `AUTO_INCREMENT`
- Foreign key constraints
- `NOT NULL` where it makes sense

### Sub-Part C — Populate with Sample Data

Insert enough data to make the queries in Sub-Part D interesting:
- At least 3 accounts with descriptive names
- At least 6 categories (a mix of income and expense)
- At least 25 transactions spread across 3 or more months, distributed across different accounts
- At least 3 transfers between accounts
- At least one account with no transactions this month
- At least one account with a negative current balance

You can use ChatGPT (or other GenAI) to help you generate realistic sample data if you wish. 

### Sub-Part D — Application Queries

Unlike Exercise 7 (QuickBite), the queries here are **organised by the application operation they support** — not just by difficulty. For each operation listed in **Section 1.2**, write the SQL query the application would execute to implement it.

For every operation, your query must be consistent with the schema you designed in Sub-Parts A and B. Each operation maps to one SQL statement (a `SELECT`, `INSERT`, `UPDATE`, or `DELETE`).

A few additional notes to guide you:

- For operations that read data involving multiple entities, think about which JOINs are needed to return all the information the application requires.
- For balance and Net Worth calculations, the values are never stored — they must be computed on the fly in SQL, just as they are in Python.
- For delete operations: consider what should happen to related rows in other tables. How will you handle this with foreign key constraints?
- For the dashboard operation (operation 26): write it as a **single query** that returns all dashboard values at once using subqueries or `UNION`.

---

## Bonus — Textual TUI

Replace the text-based TUI from Part 2 (Layer 4) with a rich terminal UI using the **Textual** library. The Textual TUI communicates with the application in exactly the same way — **exclusively via HTTP requests** to the FastAPI layer. The HTTP communication layer does not change; only the presentation changes.

The design of your Textual screens is entirely up to you. At a minimum, it should support all the same operations as the text-based TUI.

Useful resources:
- **Textual documentation**: https://textual.textualize.io/
- **GitHub**: https://github.com/Textualize/textual

---

## Suggested Directory Structure

```
hw8/
├── solution/
│   ├── __init__.py
│   ├── models/                    # dataclasses for domain entities
│   │   └── __init__.py
│   ├── repository/                # Layer 1: CSV repositories
│   │   ├── __init__.py
│   │   ├── csv_accessor.py        # CsvFileAccessor
│   │   └── base_repository.py     # BaseRepository[T]
│   ├── services/                  # Layer 2: business logic
│   │   └── __init__.py
│   ├── api/                       # Layer 3: FastAPI app + routers
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app, router registration
│   │   └── routers/               # One router module per resource
│   │       └── __init__.py
│   └── ui/                        # Layer 4: TUI
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_csv_accessor.py
│   └── test_repository/
│       └── __init__.py
├── data/                          # CSV files — created at runtime, NOT committed
├── sql/                           # Part 3: schema + data + queries
├── venv/
├── setup.cfg
├── requirements.txt
├── .gitignore
└── README.md
```

> Add `data/` to your `.gitignore`. CSV data files should not be committed.

---

## Running the Application

**Terminal 1 — Start the API:**
```bash
cd hw8
source venv/bin/activate
python -m solution.api.main
```

**Terminal 2 — Start the TUI:**
```bash
cd hw8
source venv/bin/activate
python -m solution.ui
```

Access the API documentation at `http://localhost:8000/docs`.

---

## Running Tests

```bash
cd hw8
source venv/bin/activate
pytest -v
```

## What You'll Learn

By completing this exercise you will gain practical experience with:

1. **Domain modelling** — translating real-world financial concepts into clean Python dataclasses
2. **Repository pattern** — abstracting data persistence behind a consistent interface
3. **CSV serialisation** — reading and writing structured data with Python's `csv` module
4. **Generic programming** — using `Generic[T]` to build reusable base classes
5. **Service layer design** — separating business logic from persistence and transport concerns
6. **FastAPI routers** — organising a larger API into multiple files
7. **File upload and download** — handling `UploadFile` and `FileResponse` in FastAPI
8. **Dependency injection** — passing dependencies through constructors for testability
9. **Mocking in tests** — testing layers in isolation with `unittest.mock`
10. **Relational database design** — translating a domain model into a normalised SQL schema
11. **Advanced SQL** — JOINs, subqueries, aggregations, and computed columns

---

Good luck! 💰
