# Class Exercises: Control Flow and Primitive Types

## General Requirements

- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Provide unit tests where asked using the `pytest` framework.
- All the unit tests should be in a Python package called `tests`. Use a separate Python module for each exercise test suite.
- The unit test module should be called by convention `test_<subject>.py`
- Use Type Hints for function arguments and return values
- If the functions is long (beyond 15 lines of code), divide into more functions.

---

## Exercise 1: Temperature Converter with Validation

Write a function `convert_temperature(value: float, from_unit: str, to_unit: str) -> float` that converts temperatures between Celsius, Fahrenheit, and Kelvin.

**Conversion Formulas:**
- Celsius to Fahrenheit: `F = C * 9/5 + 32`
- Fahrenheit to Celsius: `C = (F - 32) * 5/9`
- Celsius to Kelvin: `K = C + 273.15`
- Kelvin to Celsius: `C = K - 273.15`

**Validation Rules:**
- If `from_unit` or `to_unit` is not one of: "C", "F", "K", raise a `ValueError` with the message: "Invalid unit. Use 'C', 'F', or 'K'."
- If converting from Kelvin and the value is less than 0, raise a `ValueError` with the message: "Kelvin cannot be negative."
- If converting from Celsius and the value is less than -273.15, raise a `ValueError` with the message: "Temperature below absolute zero."
- If `from_unit` and `to_unit` are the same, return the original value.

**Example:**

```python
convert_temperature(0, "C", "F")  # Returns 32.0
convert_temperature(100, "C", "K")  # Returns 373.15
convert_temperature(32, "F", "C")  # Returns 0.0
convert_temperature(0, "C", "C")  # Returns 0.0
```

Write at least 3 unit tests covering different conversion scenarios and validation cases.

---

## Exercise 2: Student Grade Classifier

Write a function `classify_grade(score: int) -> str` that takes a numerical score (0-100) and returns the letter grade according to the following scale:

- 90-100: "A"
- 80-89: "B"
- 70-79: "C"
- 60-69: "D"
- 0-59: "F"

**Validation Rules:**
- If the score is less than 0 or greater than 100, raise a `ValueError` with the message: "Score must be between 0 and 100."

**Example:**

```python
classify_grade(95)  # Returns "A"
classify_grade(85)  # Returns "B"
classify_grade(55)  # Returns "F"
```

Write at least 3 unit tests covering different grade ranges and validation cases.

---

## Exercise 3: Number Pattern Generator

Write a function `generate_pyramid(height: int) -> str` that generates a number pyramid pattern. Each row should contain consecutive numbers starting from 1.

**Validation Rules:**
- If height is less than 1, raise a `ValueError` with the message: "Height must be at least 1."
- If height is greater than 9, raise a `ValueError` with the message: "Height cannot exceed 9."

**Example:**

For `height = 4`, the function should return:
```
   1
  121
 12321
1234321
```

For `height = 3`, the function should return:
```
  1
 121
12321
```

**Pattern Rules:**
- Each row contains numbers from 1 up to the row number, then back down to 1
- Each row is centered with spaces (total width = 2 * height - 1)
- The result should be a single string with rows separated by newlines

Write at least 3 unit tests covering different heights and validation cases.

---

## Exercise folder structure
```
    04_control_flow
    ├─── .vscode/
    ├─── solution/
    ├─── tests/
    ├─── venv/
    ├─── .gitignore
    ├─── exercises.md (Optional)
    └─── requirements.txt
```

## Running Your Tests

To run the tests:

```bash
cd 04_control_flow
source .\venv\Scriptsn\activate 
pytest
```

To run a specific test file (Assuming venv is activated):

```bash
pytest .\tests\test_exercise1.py 
```
