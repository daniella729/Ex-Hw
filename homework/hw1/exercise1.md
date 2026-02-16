# Homework Exercise 1: Variables and Primitive Types

## General Requirements


- The exercises must be submitted in your homework repository in a directory called `hw1` in a python package called `solution`.
- Each exercise should be implemented in a separate Python module with a given name.
- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- In the following exercises, you are not allowed to use control flow (if-else, loops, etc.); you must only utilize built-in functions that you will find in the class slides and the official documentation.
- Provide unit tests where asked using the `pytest` framework, taking examples from the tests provided for Exercises 1 and 2.
- All the unit tests should be in a Python package called `tests` under the `hw1` directory. Use a separate Python module for each exercise test suite.
- The unit test module should be called by convention `test_<subject>.py`
- Adhere to Python coding standards PEP-8
- Use Type Hints for function arguments and return values
- If the functions is long (beyond 15 lines of code), divide into more functions.
- Linting and Formatting Requirements - The Solution and the test code must be:
  - Formatted with `black` formatter before submission.


**Note**: In this exercise you are not required to pass Flake8
## Running Unit tests:

**To run the unit tests from terminal**:

1. Navigate to your homework directory `cd hw1`
2. Run `pytest tests/test_my_function.py` or simply `pytest` to run all tests



---



## Exercise 1: Parsing and Extracting from Logs

- Write a function that accepts a log line as input and returns the `pid` (process ID) as an integer.

**Example**:
**Given**: "2024-04-29 15:45:00,089 INFO [name:starwars_engine.spaceship_manager.tasks][pid:2995][uuid:20ebf460-dcdf-4b1f-abf1-7517ef3f63c2][process:run_services_if_needed_wrapper][function:run_services_if_needed][account:519][GamePlay:400004380] GamePlay's version is at least 'new' (5.2.0)."

**Expected Output**: 2995



---



## Exercise 2: Extracting Data from HTML

 - Write a function that accepts an HTML string and returns the content inside the first `<title>` tag as a string.
 - Provide two more unit tests with harder cases

**Example**:

**Given**: 

```html
<html><head><title>My Title</title></head><body></body></html>
```

**Expected Output**: The function should return: "My Title"



---



## Exercise 3: Extracting Key-Value Pairs from Logs

 - Write a function that accepts a log line and a key as input and returns the value associated with the key. (No type conversion needed.
 - Provide at least 2 unit tests with other cases

**Example**:

**Given**: 

key "account"

line: "2024-04-29 15:45:00,089 INFO [name:starwars_engine.spaceship_manager.tasks][pid:2995][uuid:20ebf460-dcdf-4b1f-abf1-7517ef3f63c2][process:run_services_if_needed_wrapper][function:run_services_if_needed][account:519][GamePlay:400004380] GamePlay's version is at least 'new' (5.2.0)."

**Expected Output**: '519'


---


## Exercise 4: Type Conversion and String Manipulation

 - Write a function that accepts a string representing a binary number and returns its decimal (base-10) integer value.
- Provide at least 2 unit tests with other cases

**Example**:

**Given**: "1101"

**Expected Output**: 13



---



## Exercise 5: Quadratic Equation

- Write a function that will receive `a`, `b`, and `c` as arguments and will solve the quadratic equation. The function will return the result as a string in the format "x1 = 3.33, x2 = 6.00", using up to 2 numbers after the decimal point.
- Provide at least 2 unit tests with other cases

**Conditions**:
- Use only arithmetic operators and built-in functions on numbers.
- No control flow (No if-else, loops, etc.).
- Do not use the `math` or `numpy` libraries.
- You can assume that discriminant is not negative.

**Example**:

**Given**: `a = 1`, `b = -3`, `c = 2`

**Expected Output**: `"x1 = 1.00, x2 = 2.00"`



---



## Exercise 6: Printing Variable Types and Their Sizes

- Write a function that prints the variable types and their sizes for all primitive types in Python. For each primitive type except boolean and NonType, provide 5 examples of variable sizes.

- No need to write unit tests for this exercise

**Example output**;

```
Type: <class 'int'>, Value: 1, Size: 28 bytes
Type: <class 'int'>, Value: 42, Size: 28 bytes
```

