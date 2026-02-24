import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import aiohttp
from typing import Any

BASE_URL = "https://jsonplaceholder.typicode.com/todos"
ITEM = 20


async def fetch_todo(session: aiohttp.ClientSession, todo_id: int) -> dict[str, Any]:
    async with session.get(f"{BASE_URL}/{todo_id}") as response:
        return await response.json()


async def main() -> None:
    print(f"Fetching {ITEM} TODO items using asyncio and aiohttp...")
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_todo(session, todo_id) for todo_id in range(1, ITEM + 1)]
        results = await asyncio.gather(*tasks)

    for todo in results:
        print(f"TODO {todo['id']}: {todo['title']}")

    execution_time = time.time() - start_time
    average_time = execution_time / ITEM

    print("\nSummary:")
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Average time per request: {average_time:.3f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
