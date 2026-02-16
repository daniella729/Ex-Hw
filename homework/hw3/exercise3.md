# Homework 3: Functions and Decorators

## General Requirements

Due date: 

- The exercises must be submitted in your homework repository in a directory called `hw3` in a python package called `solution`.
- Each exercise should be implemented in a separate Python module with a given name.
- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Do not use any third-party libraries that will just solve your exercise. The purpose is to practice the material you learned so far.
- Provide unit tests where asked using the `pytest` framework.
- All the unit tests should be in a Python package called `tests` under the `hw3` directory. Use a separate Python module for each exercise test suite.
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


**Exercise 1:** Type-Checking Function Decorator

**Description:** 
This exercise involves creating a Python decorator that ensures the arguments passed to a function and its return value adhere to specified type hints. The decorator should validate that both the inputs (`args` and `kwargs`) and the output of the function match the provided type annotations, raising a TypeError if they do not. 

### Requirements

- Implement a function decorator that checks argument and return types based on type hints.
- Utilize the `__annotations__` attribute of the function to access type hints.
- The decorator should handle the following types: `int`, `float`, `str`, `list`, `dict`, `bool`, and `NoneType`.
- In case the declared type is in the supported types list and the actual arguments provided incorrectly or the function returned an incorrect return value - the decorator should raise a `TypeError` exception with appropriate message.
- If the type is unsupported, or a type hint is not declared for the argument -  the decorator should not perform any checks for that argument.
- Ensure the decorator preserves the original function's metadata.
- Write unit tests covering various scenarios to ensure the decorator's functionality.
- Include docstrings to document the code and the decorator's behavior.

**Note:** For this exercise, passing `mypy` type checking is **not mandatory**. The focus is on understanding decorator mechanics. Type-checking decorators with dynamic attributes is advanced and can be complex. Your solution should pass `black` and `flake8` checks only.

### Expected Output

The output should be the function's result if all type checks pass. If a type mismatch occurs, the function should raise a `TypeError` with a message indicating the mismatch details (e.g., which argument is incorrect and what the expected type was).

### Example
Here's how the `type_check` decorator might be used and an example of the expected output:


```python

@type_check
def format_data(name: str, age: int, data: dict, other_info = None) -> str:
    other_info_str = ', Other Info : ' + str(other_info) if other_info else ''
    return f"Name: {name}, Age: {age}, Data: {data['key']}{other_info_str}"

# Test the function with correct types
print(format_data("Alice", 30, {"key": "value"}, 1234))

# Test the function with incorrect types
print(format_data("Alice", "thirty", {"key": "value"}))
```

#### Output

```plaintext
Name: Alice, Age: 30, Data: value, Other Info : 1234

TypeError: Argument 'age' must be of type <class 'int'>, got <class 'str'> instead.
```

**Exercise 2:** Fibonacci Calculator Without Loops

**Description:**
The Fibonacci sequence is a famous mathematical sequence where each number is the sum of the two preceding numbers. The sequence starts: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

In this exercise, you will implement a function that calculates the nth Fibonacci number without using any loops (no `for`, `while`, etc.). Your implementation must be efficient enough to handle large values of n (up to 200).

### Requirements

- Implement a function `fibonacci(n: int) -> int` that returns the nth Fibonacci number.
- The function must NOT use any loop constructs (`for`, `while`, etc.).
- The function must handle values of n from 1 to 200 efficiently.
- Use the convention: `fibonacci(1) = 0`, `fibonacci(2) = 1`, `fibonacci(3) = 1`, etc.
- The function should raise a `ValueError` if n is less than 1.
- Write comprehensive unit tests using `pytest` to verify correctness.
- Include parameterized tests for multiple values of n.
- Include docstrings to document the code.

### Expected Output

The function should return the nth Fibonacci number as an integer. For large values of n, the numbers will be very large but should still be computed efficiently.

### Example

```python
print(fibonacci(1))   # Output: 0
print(fibonacci(2))   # Output: 1
print(fibonacci(10))  # Output: 34
```

### Hint

You might want to use the `functools.lru_cache` decorator.
