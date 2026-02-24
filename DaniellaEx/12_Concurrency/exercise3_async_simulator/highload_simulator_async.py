import time
from typing import List
import statistics
import asyncio
import aiohttp
import uuid

# Constants
NUM_REQUESTS = 20
BAD_HANDLER_URL = (
    "http://localhost:8000/process_order?user_id=123&product_id=456&zip_code=12345"
)

GOOD_HANDLER_URL = (
    "http://localhost:8001/process_order?user_id=123&product_id=456&zip_code=12345"
)


async def make_request(session: aiohttp.ClientSession, url: str) -> float:
    """Make a single request and return the time taken."""
    request_id = uuid.uuid4().hex[:5]
    start_time = time.time()
    async with session.get(url) as response:
        response.raise_for_status()
    duration = time.time() - start_time
    print(f"Task {request_id} finished in {duration:.3f}s")
    return duration


async def run_load_test(url: str, description: str) -> None:
    """Run load test against specified URL and print results."""
    times: List[float] = []

    print(f"\nTesting {description}...")
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [make_request(session, url) for _ in range(NUM_REQUESTS)]
        times = await asyncio.gather(*tasks)

    total_time = time.time() - start_time

    print(f"Results for {description}:")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average request time: {statistics.mean(times):.3f} seconds")
    print(f"Median request time: {statistics.median(times):.3f} seconds")
    print(f"Max request time: {max(times):.3f} seconds")
    print(f"Min request time: {min(times):.3f} seconds")
    print(f"Requests per second: {NUM_REQUESTS/total_time:.2f}")


async def main() -> None:
    """Run load tests against both good and bad handlers."""
    print("Starting load test simulation...")

    # Test bad/good handler
    await run_load_test(BAD_HANDLER_URL, "Bad Handler (blocking requests)")
    await run_load_test(GOOD_HANDLER_URL, "Good Handler (blocking requests)")


if __name__ == "__main__":
    asyncio.run(main())
