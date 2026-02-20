# Homework 4: Budget Planner CLI Application

## General Requirements

- The exercises must be submitted in your homework repository in a directory called `hw4` in a python package called `solution`.
- Each exercise should be implemented in a separate Python module with a given name.
- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Provide unit tests where asked using the `pytest` framework.
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
- Exercise directory structure should look like this:
```
hw4/
├── solution/
│   ├── __init__.py
│   ├── budget.py         # Business logic (classes for Budget, Income, Expense)
│   ├── cli.py            # Command-line interface (UI layer)
│   └── main.py           # Entry point for the application
├── tests/
│   ├── __init__.py
│   ├── test_budget.py    # Tests for business logic
│   └── test_cli.py       # Tests for CLI logic (optional)
├── venv/                 # Your virtual environment (should be in .gitignore and not committed)
├── setup.cfg             # Linter configuration file
├── requirements.txt      # Dependencies (textual, pytest, etc.)
├── lint.sh               # Optional script to run linters
├── lint.ps1              # Optional script to run linters on Windows
├── .gitignore            # Optional, to ignore virtual environment and other files
└── README.md             # Optional, instructions on how to run the application
```

---

## Exercise: Budget Planner CLI Application

### Description

Create a **Budget Planner** command-line application that allows users to manage their monthly income and expenses. The application should help users track their financial information and calculate their remaining budget for the month.

This exercise focuses on practicing **Object-Oriented Programming (OOP)** with classes and **separation of concerns** by keeping the user interface separate from the business logic.

### Required Features

Your Budget Planner application must implement the following features:

1. **Add Income Sources**
   - The user should be able to add multiple income sources with their amounts.
   - Each income source should have a description (e.g., "Salary", "Freelance work") and an amount.

2. **Add Expenses**
   - The user should be able to add multiple expenses with their amounts.
   - Each expense should have a description (e.g., "Rent", "Groceries", "Transportation") and an amount.

3. **View Summary**
   - The user should be able to view a summary of their budget that includes:
     - List of all income sources with their amounts
     - List of all expenses with their amounts
     - Total income (sum of all income sources)
     - Total expenses (sum of all expenses)
     - Remaining budget (total income - total expenses)

4. **Remove Income or Expense**
   - The user should be able to remove a specific income source or expense by its description or index.

5. **Clear All Data**
   - The user should be able to clear all income and expense entries to start fresh.

6. **Interactive Menu**
   - The application should provide an interactive menu with clear options for all available actions.
   - The menu should continue to display until the user chooses to exit.
   - If you choose not to use a Third party for (TUI Textual User interface) you can implement a simple text-based menu using `input()` and `print()`. For example print the menu options in a while loop and use `input()` to get the user's choice. Each menu item should have a number that the user can enter to select that option.

7. **Input Validation**
   - The application should validate user input and handle errors gracefully.
   - Examples: negative amounts, invalid menu choices, non-numeric amounts.

### Technical Requirements

1. **Use Classes for Business Logic**
   - Create classes to represent the core concepts of your application (e.g., `Income`, `Expense`, `Budget`).
   - The business logic should be completely independent of the user interface.
   - All business logic classes should be in a separate module (e.g., `budget.py`).

2. **Separate User Interface**
   - Implement the Command-Line Interface (CLI) in a separate module (e.g., `cli.py`).
   - The CLI module should handle all user interactions (input/output).
   - The CLI should use the business logic classes to perform operations.

3. **Entry Point**
   - Create a `main.py` module that serves as the entry point for your application.
   - This module should initialize the application and start the CLI.

4. **Unit Tests**
   - Write comprehensive unit tests for your business logic classes.
   - Test all methods in your classes, including edge cases.
   - Tests should cover scenarios like:
     - Adding income and expenses
     - Calculating totals correctly
     - Removing items
     - Handling invalid inputs
   - You are encouraged but not required to write tests for the CLI module.

5. **Type Hints**
   - All functions and methods must have type hints for arguments and return values.

6. **Documentation**
   - Include docstrings for all classes and methods.
   - Provide clear descriptions of what each class and method does.

### User Interface Options

You have flexibility in how you build the command-line interface:

#### Option 1: Basic CLI (using `input()` and `print()`)
- Use Python's built-in `input()` function to get user input.
- Use `print()` to display information to the user.
- Create a simple text-based menu.

**Example interaction:**
```
===== Budget Planner =====
1. Add Income
2. Add Expense
3. View Summary
4. Remove Income
5. Remove Expense
6. Clear All Data
7. Exit

Choose an option: 1
Enter income description: Salary
Enter income amount: 5000
Income added successfully!
```

#### Option 2: Advanced CLI (using Textual library)
- Use the **Textual** library to create a more sophisticated terminal user interface.
- Textual provides rich text formatting, colors, and interactive widgets.
- GitHub: https://github.com/Textualize/textual
- Documentation: https://textual.textualize.io/

**Installation:**
```bash
pip install textual
```

**Note:** Using Textual is optional but recommended if you want to explore a modern TUI (Text User Interface) framework. If you choose Textual, you'll need to add it to your `requirements.txt` file. You can choose other TUI libraries if you prefer, but make sure to include them in your `requirements.txt` file and document how to run the application with those libraries in your README.md.

### Example Output

Here's an example of what the summary view might look like:

```
====================================
        BUDGET SUMMARY
====================================

INCOME SOURCES:
  1. Salary                   $5,000.00
  2. Freelance Work          $1,500.00
  3. Investment Returns        $300.00
------------------------------------
TOTAL INCOME:                $6,800.00

EXPENSES:
  1. Rent                    $1,500.00
  2. Groceries                 $400.00
  3. Transportation            $200.00
  4. Utilities                 $150.00
  5. Entertainment             $100.00
------------------------------------
TOTAL EXPENSES:              $2,350.00

====================================
REMAINING BUDGET:            $4,450.00
====================================
```

### Tips for Success

1. **Start with the Business Logic**
   - Design and implement your classes first (e.g., `Income`, `Expense`, `Budget`).
   - Write unit tests for these classes before implementing the UI.
   - This approach follows Test-Driven Development (TDD) principles.

2. **Keep It Simple**
   - Start with basic functionality and add features incrementally.
   - You don't need to implement data persistence (saving to files) unless you want to challenge yourself.

3. **Separation of Concerns**
   - Your business logic should NOT contain any `input()` or `print()` statements.
   - Your CLI module should NOT contain business logic (calculations, data management).
   - This separation makes your code more testable and maintainable.

4. **Handle Edge Cases**
   - What happens if a user tries to remove an income that doesn't exist?
   - What if the user enters a negative amount?
   - What if the user enters text instead of a number?

5. **Use Descriptive Names**
   - Choose clear, meaningful names for your classes, methods, and variables.

6. **Test Thoroughly**
   - Write tests before or alongside your implementation.
   - Test both happy paths (expected behavior) and edge cases (errors, invalid input).

### Running Your Application

To run your application from the terminal:

```bash
cd hw4
source venv/bin/activate  # On Windows: source venv/Scripts/activate
python solution/main.py
```

### Running Unit Tests

To run your unit tests:

```bash
cd hw4
source venv/bin/activate  # On Windows: source venv/Scripts/activate
pytest
```

### Linting and Formatting
Before submitting your code, make sure to run the linters and formatter:

```bash
cd hw4
source venv/bin/activate  # On Windows: source venv/Scripts/activate
lint.sh  # Or lint.ps1 on Windows
```

### Optional Enhancements

If you finish the required features and want to challenge yourself further, consider adding:

- **Data Persistence**: Save and load budget data to/from a JSON file. Use the web (or ChatGPT) to understand how to read/write JSON files in Python.
- **Budget Categories**: Group expenses by categories (e.g., Housing, Food, Transportation).
- **Date Tracking**: Track when each income or expense was added.
- **Budget Goals**: Allow users to set spending limits for different categories.
- **Reporting**: Generate monthly reports showing spending trends.
- **Edit Functionality**: Allow users to edit existing income or expense entries.

Good luck, and happy coding! 💰
