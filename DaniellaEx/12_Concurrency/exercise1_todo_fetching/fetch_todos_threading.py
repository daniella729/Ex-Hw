from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time
from typing import Any

BASE_URL = "https://jsonplaceholder.typicode.com/todos"
ITEM = 20


def fetch_todo(todo_id: int) -> dict[str, Any]:
    try:
        respone = requests.get(f"{BASE_URL}/{todo_id}")
    except requests.exceptions.ConnectionError:
        print(f"Failed to fetch TODO {todo_id}")
    return respone.json()


if __name__ == "__main__":
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_todo, item) for item in range(1, ITEM + 1)]
        for future in as_completed(futures):
            todo = future.result()
            print(f"TODO {todo["id"]}:{todo["title"]}")
    print("\nSummary:")
    execution_time = time.time() - start_time
    average_time_per_request = execution_time / ITEM

    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Average time per request: {average_time_per_request:.2f} seconds")
