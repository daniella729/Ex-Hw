def quadratic_equation(a: float, b: float, c: float) -> str:
    """Solve a quadratic equation using the formula and return both roots formatted to 2 decimals"""
    delta = b**2 - 4 * a * c
    sqrt_delta = delta**0.5
    x1 = (-b + sqrt_delta) / (2 * a)
    x2 = (-b - sqrt_delta) / (2 * a)
    return f"x1={x1:.2f}, x2={x2:.2f}"
