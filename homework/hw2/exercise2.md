# Homework 2: Control Flow

## General Requirements

- The exercises must be submitted in your homework repository in a directory called `hw2` in a python package called `solution`.
- Each exercise should be implemented in a separate Python module with a given name.
- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Do not use any third-party libraries that will just solve your exercise. The purpose is to practice the material you learned so far.
- Provide unit tests where asked using the `pytest` framework.
- All the unit tests should be in a Python package called `tests` under the `hw2` directory. Use a separate Python module for each exercise test suite.
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
hw<number>/
├── solution/
│   ├── __init__.py
│   Solution code files and packages here
├── tests/
│   ├── __init__.py
│   test files here
├── venv/  # Your virtual environment (should be in .gitignore and not committed) 
├── setup.cfg  # Linter configuration file
├── requirements.txt  # If needed for test dependencies
├── lint.sh  # Optional script to run linters
├── lint.ps1  # Optional script to run linters on Windows
├── .gitignore  # Optional, to ignore virtual environment and other files
```


## Exercise 1: Log Content Analyzer

**Exercise:**
Create a function `analyze_log_content(log_content: str) -> dict` that processes log content provided as a string, counting the number of error, warning, and info messages. Utilize structural pattern matching to solve this exercise.

- **Given:**
  - Input: string containing multiple lines of log entries. Each log entry begins with a timestamp followed by a log level ("ERROR", "WARNING", "INFO"), and includes detailed metadata and a message.
  The input might contain also lines without any of the mentioned log levels, you should ignore them.
  
- **Expected output:**
  - A dictionary with keys 'Error', 'Warning', and 'Info', representing the count of each type of log entry.

**Requirements:**
- Include type hints in the function declaration.
- Write at least two unit tests for the function.

**Example**

```
log_content = """
2024-04-29 15:45:00,089 INFO [name:starwars_engine][pid:2995] Message one
2024-04-29 15:45:05,123 WARNING [name:starwars_engine][pid:2996] Check disk space
2024-04-29 15:45:08,111 /var/log/apache2/server.access.log 172.18.0.12 - - "POST /api/command/?201dfd68-e48d-587b-e715-3ff83ef3af19 HTTP/1.1" 200
2024-04-29 15:45:10,456 ERROR [name:starwars_engine][pid:2997] Failed to start engine
2024-04-29 15:46:00,789 INFO [name:starwars_engine][pid:2998] All systems go
"""
```

**Expected Output**: 

```
{
    'Error': 1, 
    'Warning': 1, 
    'Info': 2
}
```

---

## Exercise 2: Simple Python Calculator

Develop a simple command-line calculator in Python that performs basic arithmetic operations: addition, subtraction, multiplication, and division. 

### Requirements:

You are expected to create a program that can:

- Continuously accept user input until the user decides to exit.
- Prompt the user to write the operation in a human readable form - Examples:
  - "add 2 t0 5" 
  - "subtract 2 from 5"
  - "multiply 2 by 5"
  - "divide 10 by 5"
  - "help"
  - "exit"
- When the user types "help" The program should display instructions for the user on how to interact with it.
- When the user enters a valid operation - Display the result of the operation.
  - Example: "add 2 t0 5" display "The answer is 7"
- When the user enters invalid operation - Display "invalid operation"
- Handle basic error checking, such as division by zero and invalid inputs.
- Divide your code into multiple functions.
- Include type hints in functions declarations.
- Write unit tests that should cover all your logic, except the part that asks for user input. Think how to organize your code, so it will be more convenient to test it. 
- Advice: Go TDD. first write the tests and then proceed to implementation.
- Advice: Use parameterized tests, to test multiple cases

---

## Exercise 3: Git CLI Command Simulator

**Exercise Description:**

Create a Python function named `git_command_simulator` that interprets and responds to various Git command strings using structural pattern matching introduced in Python 3.10. This function should simulate actions related to Git commands by returning a descriptive string of what each command would do.

### Requirements:

- You must support all git commands provided in the `git_commands.csv` file. (You do not need to read the file from the OS, just use its content)
- Your tests should cover all the commands and edge cases. Advice - Use parameterized tests. 
- Do not use "magic strings". Define constants according to PEP8 naming conventions.
- Commands that includes repository url, must check that given url is in the valid pattern. 
- Do not use any third party libs for command line parsing. The purpose is for you to practice pattern matching.

### Given

A Git command as a sting. 

### Expected Output:

The function should return a string describing the action corresponding to the Git command it received.
If the given string is not a supported command return "Invalid Command"

### Example:

#### Example Input:
```python
command = 'git rm --cached readme.md'
```

#### Example Output:
```python
'Unstage file readme.md while retaining the changes in the working directory.'
```
