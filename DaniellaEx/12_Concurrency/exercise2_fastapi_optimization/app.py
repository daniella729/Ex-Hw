import time
import uvicorn
from fastapi import FastAPI
from typing import Any

app = FastAPI(title="Order Processing API", version="1.0.0")

USER_FETCH_DELAY = 0.5
INVENTORY_FETCH_DELAY = 0.3
SHIPPING_FETCH_DELAY = 0.4
PAYMENT_PROCESSING_DELAY = 0.2
FIBONACCI_INDEX = 30
SERVER_PORT = 8000


def calculate_fibonacci(index: int) -> int:
    """CPU-bound operation: Calculate nth Fibonacci number recursively."""
    if index <= 1:
        return index
    return calculate_fibonacci(index - 1) + calculate_fibonacci(index - 2)


def fetch_user_data(user_id: int) -> dict[str, Any]:
    """Simulates I/O-bound operation: Fetch user data from external service."""
    time.sleep(USER_FETCH_DELAY)  # Simulate network delay
    return {
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
    }


def fetch_inventory_data(product_id: int) -> dict[str, Any]:
    """Simulates I/O-bound operation: Fetch inventory from database."""
    time.sleep(INVENTORY_FETCH_DELAY)  # Simulate database query delay
    return {"product_id": product_id, "stock": 100, "warehouse": "Warehouse A"}


def fetch_shipping_options(zip_code: str) -> list[dict[str, Any]]:
    """Simulates I/O-bound operation: Fetch shipping options from external service."""
    time.sleep(SHIPPING_FETCH_DELAY)  # Simulate API call delay
    return [
        {"method": "Standard", "cost": 5.99, "days": 5},
        {"method": "Express", "cost": 15.99, "days": 2},
        {"method": "Overnight", "cost": 29.99, "days": 1},
    ]


@app.get("/process_order")
async def process_order(user_id: int, product_id: int, zip_code: str) -> dict:
    """
    Process an order by:
    1. Fetching user data
    2. Fetching inventory data
    3. Fetching shipping options
    4. Calculating shipping discount (CPU-intensive)
    """

    # Problem 1: Sequential I/O operations (should be concurrent)
    user = fetch_user_data(user_id)
    inventory = fetch_inventory_data(product_id)
    shipping = fetch_shipping_options(zip_code)

    # Problem 2: CPU-intensive operation blocking the event loop
    # Calculate discount based on Fibonacci (artificially expensive)
    discount_factor = calculate_fibonacci(FIBONACCI_INDEX) % 10

    # Problem 3: More sequential operations
    time.sleep(PAYMENT_PROCESSING_DELAY)  # Simulate payment processing

    return {
        "user": user,
        "product": inventory,
        "shipping_options": shipping,
        "discount_percent": discount_factor,
        "status": "processed",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
