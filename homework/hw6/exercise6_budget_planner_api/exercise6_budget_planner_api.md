# Homework 6: Budget Planner REST API

## General Requirements

- The exercises must be submitted in your homework repository in a directory called `hw6` in a python package called `solution`.
- Each exercise should be implemented in a separate Python module with a given name.
- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- If the functions is long (beyond 15 lines of code), divide into more functions.
- Linting and Formatting Requirements - The Solution and the test code must be:
  - Formatted with `black` formatter before submission.
  - Pass `flake8` checks before submission.
  - Pass `mypy` type checks before submission.
- Navigate to the `linter-config` directory to find the `setup.cfg` file with the linters configuration. Copy all files to the root of your exercise directory to use the same configuration for your exercises.
- Remember to run flake8 from the root of your exercise directory to ensure it picks up the correct configuration, otherwise you will suffer from the cruelty of the default WPS rules.
- Exercise directory structure should look like this:
```
hw6/
├── solution/
│   ├── __init__.py
│   ├── Your solution code files (e.g., budget_planner.py, etc...)
├── tests/
│   ├── __init__.py
│   └── your test files (e.g., test_budget_planner.py, etc...)
├── venv/                      # Your virtual environment (should be in .gitignore)
├── setup.cfg                  # Linter configuration file
├── requirements.txt           # Dependencies (FastAPI, uvicorn, requests, pytest, etc.)
├── lint.sh                    # Optional script to run linters
├── lint.ps1                   # Optional script to run linters on Windows
├── .gitignore                 # Optional, to ignore virtual environment and other files
└── README.md                  # Optional, instructions on how to run the application
```

---

## Exercise: Budget Planner REST API

### Description

This exercise extends your **Budget Planner** application from Exercise 4 by adding two critical components:

1. **REST API Layer** - Expose your budget planner functionality through HTTP endpoints using FastAPI
2. **UI Separation** - Decouple the TUI from the business logic by having it communicate via HTTP requests

This exercise focuses on **layered architecture**, **separation of concerns**, and **building web APIs** with FastAPI.

### Prerequisites

**CRITICAL**: This exercise must be started ONLY after you have successfully completed Exercise 4 (Budget Planner CLI Application). You should have a fully working budget planner with a TUI (Text User Interface: Optinon1 or Option2) and all required business logic.

### Getting Started

1. Copy all your code from Exercise 4 (`hw4/`) to the new `hw6/` directory.
2. You will be adding new modules and functionality on top of your existing implementation.
3. The goal is to add the FastAPI layer without modifying your existing business logic classes.
4. **Note**: Data will continue to be stored in memory as in Exercise 4.

---

## Part 1: REST API for Budget Planner

### Description

Create a REST API layer for your Budget Planner using the **FastAPI** web framework. The API should expose all the operations that are currently available in your business logic layer through HTTP endpoints.

### Requirements

1. **Separate API Module**
   - Create a new module called `budget_planner_api.py` for your FastAPI application entry point.
   - The API layer should be completely separate from your business logic.
   - Import and use your existing business logic classes - Try NOT to modify them.

2. **Implement HTTP Endpoints**
   - Create RESTful API endpoints for all operations in your budget planner:
     - **POST /income** - Add a new income source
     - **DELETE /income/{id}** - Delete an income source by ID
     - **POST /expense** - Add a new expense
     - **DELETE /expense/{id}** - Delete an expense by ID
     - **GET /summary** - Get budget summary (total income, total expenses, remaining budget)
     - **DELETE /clear** - Clear all data

3. **Documentation**
   - FastAPI automatically generates interactive API documentation.
   - Access the docs at `http://localhost:8000/docs` when your API is running.

4. **Running the API**
   - Your `budget_planner_api.py` should be executable and start the FastAPI server.
   - Use `uvicorn` to run the application.

### Manual Testing for Part 1

Run your FastAPI application:

```bash
cd hw6
source venv/bin/activate  # On Windows: source venv/Scripts/activate
python solution/budget_planner_api.py
```

Your API should start and be accessible at `http://localhost:8000`.

Test your endpoints using:
- **Swagger UI**: Navigate to `http://localhost:8000/docs` in your browser
- **Postman**: Create requests to test each endpoint
- **curl**: Use curl commands from the terminal

Example curl commands:
```bash
# Add income
curl -X POST "http://localhost:8000/income" -H "Content-Type: application/json" -d '{"description": "Salary", "amount": 5000}'

# Get all income
curl "http://localhost:8000/income"

# Get summary
curl "http://localhost:8000/summary"

# Delete income by ID
curl -X DELETE "http://localhost:8000/income/1"
```

### Important Notes

- **No Tests Required**: You are NOT required to write tests for the FastAPI layer at this point. We haven't covered testing FastAPI applications yet.
- **Keep Business Logic Unchanged**: Ideally, you should not need to modify your business logic code from Exercise 4. Just import and use it in your API routes.

---

## Part 2: UI Separation for the Budget Planner

### Description

Currently, your TUI (Text User Interface) imports and uses the business logic layer directly. In this part, you'll completely separate the UI from the business logic by making the UI communicate with the API layer via HTTP requests.

### Requirements

1. **Update UI Module**
   - Modify your `budget_planner_ui.py` (or whatever you called your UI module in Exercise 4) to use HTTP requests instead of direct imports.
   - Remove all imports of business logic modules.
   - Use the `requests` library to send HTTP requests to your API endpoints.

2. **HTTP Communication**
   - For each menu option in your UI, send the appropriate HTTP request to the API.
   - Parse the JSON responses to appropiate data classes and display them to the user.
   - Handle HTTP errors gracefully and display meaningful messages to users. (use try-except blocks)

3. **API Base URL**
   - Make the API base URL configurable (e.g., `http://localhost:8000`).
   - Define it as a constant in your UI module.

4. **Error Handling**
   - Handle connection errors (API not running, network issues).
   - Display user-friendly error messages. (Define messages as constants)
   - Handle HTTP error responses appropriately.

### Manual Testing for Part 2

Run both the API and UI as separate processes:

**Terminal 1 - Start the API:**
```bash
cd hw6
source venv/bin/activate  # On Windows: source venv/Scripts/activate
python solution/budget_planner_api.py
```

**Terminal 2 - Start the UI:**
```bash
cd hw6
source venv/bin/activate  # On Windows: source venv/Scripts/activate
python solution/budget_planner_ui.py
```

Every menu option in the UI should now send HTTP requests to the API and display responses in the console.

Test the following scenarios:
1. Start the UI without starting the API - verify error messages are displayed
2. Start both API and UI - verify all menu options work correctly
3. Stop the API while the UI is running - verify error handling works

### BONUS: Write Unit Tests for the UI functions

- Use `responses` library to mock HTTP responses from the API in your UI tests.


### Important Notes

- **Two Separate Processes**: The API and UI run as separate Python processes. They communicate only via HTTP.
- **Complete Separation**: The UI should have NO direct dependency on the business logic layer - only HTTP communication with the API.

---

## Architecture Overview

After completing both parts, your application will have a clean layered architecture:

```
┌─────────────────────────────────────┐
│  UI Layer (budget_planner_ui.py)    │
│  - Text User Interface (TUI)        │
│  - HTTP requests to API             │
└──────────────┬──────────────────────┘
               │ HTTP (requests library)
               ▼
┌─────────────────────────────────────┐
│  API Layer (budget_planner_api.py)  │
│  - FastAPI routes                   │
│  - Request/Response models          │
└──────────────┬──────────────────────┘
               │ Function calls
               ▼
┌─────────────────────────────────────┐
│  Business Logic (budget.py)         │
│  - Transaction, Category classes    │
│  - Business rules and calculations  │
│  - In-memory data storage           │
└─────────────────────────────────────┘
```

---

## Tips

1. **Work Incrementally**
   - Complete Part 1 first and test it thoroughly before moving to Part 2.
   - Use Swagger UI to test all your API endpoints before working on the UI.

2. **Keep Layers Separate**
   - Each layer should have a single responsibility.
   - Avoid mixing concerns (e.g., don't put business logic in your API routes).
   - The API layer should only handle HTTP requests/responses and delegate to business logic.
   - The UI layer should only handle user interaction and HTTP communication.

3. **Read the Documentation**
   - **FastAPI**: https://fastapi.tiangolo.com/ (refer to the Tutorial section)
   - **Requests**: https://requests.readthedocs.io/

4. **Do not use Pydantic models for now**
   - For simplicity, you can use plain dictionaries for request/response data in your API routes. We didn't cover Pydantic models yet, so it's not required. 


---

## Running Your Application

### Option A: Run API Only (for testing endpoints)

```bash
cd hw6
source venv/bin/activate  # On Windows: source venv/Scripts/activate
python solution/budget_planner_api.py
```

Access the API documentation at `http://localhost:8000/docs`

### Option B: Run Both API and UI (full application)

**Terminal 1 - Start the API:**
```bash
cd hw6
source venv/bin/activate
python solution/budget_planner_api.py
```

**Terminal 2 - Start the UI:**
```bash
cd hw6
source venv/bin/activate
python solution/budget_planner_ui.py
```

---

## Running Unit Tests

```bash
cd hw6
source venv/bin/activate  # On Windows: source venv/Scripts/activate
pytest -v
```

Note: You'll only have tests for the business logic from Exercise 4. Tests for the API and UI are not required.


## What You'll Learn

By completing this exercise, you will gain practical experience with:

1. **Building REST APIs** with FastAPI
2. **Layered Architecture** and separation of concerns
3. **HTTP Communication** between processes
4. **API Design** and RESTful principles
5. **Error Handling** in web applications
6. **Interactive API Documentation** with Swagger UI
7. **Client-Server Architecture** patterns

---

Good luck, and enjoy building your Budget Planner API! 🚀
