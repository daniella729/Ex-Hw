# Class Exercises: Primitive Types & Operators

## General Instructions

- These exercises are designed to help you experiment with Python's primitive types and operators.
- Write each exercise as a simple Python script (`.py` file).
- Do not use functions, classes, if-else statements, or loops - just simple variable assignments and expressions.
- Use `input()` to get user input and `print()` to display your results.
- Remember: `input()` always returns a string, so use `int()` or `float()` to convert to numbers.
- Add type hints where appropriate to practice type annotations.

---

## Exercise 1: Temperature Converter

**Goal**: Practice with primitive types, arithmetic operators, type conversion, and user input.

Write a Python script called `temperature_converter.py` that:

1. Prompts the user to enter a temperature in Celsius
2. Converts the input string to a float using `float()`
3. Converts the temperature from Celsius to Fahrenheit using the formula: `F = (C × 9/5) + 32`
4. Converts the temperature from Celsius to Kelvin using the formula: `K = C + 273.15`
5. Prints all three temperatures with descriptive labels

**Example Run**:
```
Enter temperature in Celsius: 25.0
Temperature in Celsius: 25.0
Temperature in Fahrenheit: 77.0
Temperature in Kelvin: 298.15
```

**Hints**:
- Use `input()` to get user input (returns a string)
- Use `float()` to convert the string to a decimal number
- Use the `*` operator for multiplication
- Use the `/` operator for division
- Use the `+` operator for addition

---

## Exercise 2: Rectangle Measurements

**Goal**: Practice with arithmetic operators, multiple calculations, and user input.

Write a Python script called `rectangle_measurements.py` that:

1. Prompts the user to enter the width of a rectangle
2. Prompts the user to enter the height of a rectangle
3. Converts both inputs to floats
4. Calculates the area of the rectangle: `area = width × height`
5. Calculates the perimeter of the rectangle: `perimeter = 2 × (width + height)`
6. Calculates the diagonal of the rectangle using the Pythagorean theorem: `diagonal = √(width² + height²)`
   - Hint: You can calculate square root using the power operator: `x ** 0.5`
7. Prints all measurements with descriptive labels

**Example Run** (for width=12.5, height=8.0):
```
Enter the width of the rectangle: 12.5
Enter the height of the rectangle: 8.0
Width: 12.5
Height: 8.0
Area: 100.0
Perimeter: 41.0
Diagonal: 14.84082207965583
```

**Hints**:
- Use `input()` to get user input
- Use `float()` to convert strings to decimal numbers
- Use `**` for exponentiation (e.g., `x ** 2` for squaring)
- Use `** 0.5` for square root

---

## Exercise 3: Boolean Logic and Comparisons

**Goal**: Practice with comparison operators, logical operators, boolean expressions, and user input.

Write a Python script called `logic_expressions.py` that:

1. Prompts the user to enter three integer numbers (a, b, and c)
2. Converts the inputs to integers using `int()`
3. Evaluates and prints the following boolean expressions with descriptive labels:
   - Is `a` equal to `c`?
   - Is `a` less than `b`?
   - Is `b` greater than or equal to `a`?
   - Is `a` not equal to `b`?
   - Are both conditions true: `a < b` AND `b > c`?
   - Is at least one condition true: `a > b` OR `a == c`?
   - Is it NOT true that `a` equals `b`?

4. Prompts the user to enter two words (strings)
5. Evaluates and prints:
   - Are the strings equal?
   - Are the strings equal when comparing lowercase versions? (Hint: use `.lower()` method)
   - What is the length of the first word? (Hint: use `len()` function)

**Example Run**:
```
Enter first number (a): 10
Enter second number (b): 20
Enter third number (c): 10
a = 10, b = 20, c = 10

Is a equal to c? True
Is a less than b? True
Is b greater than or equal to a? True
Is a not equal to b? True
Are both a < b AND b > c true? True
Is at least one true: a > b OR a == c? True
Is it NOT true that a equals b? True

Enter first word: Python
Enter second word: python
word1 = Python, word2 = python

Are the strings equal? False
Are the strings equal (lowercase)? True
Length of word1: 6
```

**Operators to use**:
- Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical operators: `and`, `or`, `not`

**Hints**:
- Use `int()` to convert string input to integers
- String inputs don't need conversion - `input()` already returns strings

---

## Additional Challenge (Optional)

Create a script called `number_properties.py` that:

1. Prompts the user to enter an integer number
2. Converts the input to an integer using `int()`
3. Prints:
   - The number itself
   - Its type using `type()`
   - Its size in bytes using `sys.getsizeof()` (you'll need to `import sys` at the top)
   - The number squared
   - The number as a float
   - The number as a string
   - Whether the number is greater than 0 (boolean result)

**Example Run**:
```
Enter an integer: 42
Number: 42
Type: <class 'int'>
Size in bytes: 28
Number squared: 1764
As float: 42.0
As string: 42
Is positive: True
```
