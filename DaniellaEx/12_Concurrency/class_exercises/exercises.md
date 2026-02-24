# Class Exercises: Concurrency

## General Requirements

- Do not use any Generative-AI (like ChatGPT) tools to solve these exercises. The purpose is to practice your own skills. You can use Generative-AI tools to help you understand concepts, but not to generate the solution code.
- Linting and Formatting Requirements - The Solution and the test code must be:
  - Formatted with `black` formatter before submission.
  - Pass `flake8` checks before submission.
  - Pass `mypy` type checks before submission.

---

## Exercise 1: Concurrent Fetching of TODO Items

**Description:**
Implement three Python programs that fetch TODO items from the JSONPlaceholder API concurrently. Each program will use a different concurrency approach to fetch 20 TODO items and print their titles. This exercise demonstrates the differences between threading, multiprocessing, and asyncio approaches to concurrency.

**Learning Objectives:**
- Understand different concurrency models in Python
- Compare thread-based, process-based, and async-based concurrency
- Work with external APIs using different HTTP libraries
- Measure and compare performance across different approaches

**API Information:**
- Base URL: `https://jsonplaceholder.typicode.com/todos/<number>`
- Replace `<number>` with TODO item IDs from 1 to 20
- Example: `https://jsonplaceholder.typicode.com/todos/1`
- Each request returns a JSON object with fields: `id`, `title`, `completed`, `userId`

**Common Requirements for All Programs:**
- Fetch TODO items with IDs from 1 to 20 (20 total items)
- Print the title of each TODO item as it's fetched
- Measure and display the total execution time
- Handle potential errors gracefully (network errors, invalid responses)
- Include type hints for all functions
- Add a `if __name__ == "__main__":` guard for the main execution

---

### Part 1: ThreadPoolExecutor Implementation

**Requirements:**
- Create a program named `fetch_todos_threading.py`
- Use `concurrent.futures.ThreadPoolExecutor` for concurrency
- Use the `requests` library for HTTP requests (you'll need to install it: `pip install requests`)
- Create a function `fetch_todo(todo_id: int) -> dict[str, Any]` that fetches a single TODO item
- Use ThreadPoolExecutor with `max_workers=8` to fetch all 20 items concurrently
- Print each TODO title as it's received
- Measure execution time using `time.time()`
- Print summary statistics: total time, average time per request

**Example Output:**
```
Fetching 20 TODO items using ThreadPoolExecutor...
TODO 3: fugiat veniam minus
TODO 1: delectus aut autem
TODO 2: quis ut nam facilis et officia qui
TODO 5: laboriosam mollitia et enim quasi adipisci quia provident illum
...
TODO 20: ullam nobis libero sapiente ad optio sint

Summary:
Total execution time: 0.85 seconds
Average time per request: 0.043 seconds
```

**Hints:**
- Use `executor.submit()` to submit tasks and collect futures
- Use `concurrent.futures.as_completed()` to process results as they complete

---

### Part 2: ProcessPoolExecutor Implementation

**Requirements:**
- Create a program named `fetch_todos_multiprocessing.py`
- Use `concurrent.futures.ProcessPoolExecutor` for concurrency
- Use the `requests` library for HTTP requests
- Create a function `fetch_todo(todo_id: int) -> dict[str, Any]` that fetches a single TODO item
- Use ProcessPoolExecutor with `max_workers=8` to fetch all 20 items concurrently
- Print each TODO title as it's received
- Measure execution time and print summary statistics

**Important Notes:**
- ProcessPoolExecutor creates separate Python processes, which have more overhead than threads
- For I/O-bound tasks like HTTP requests, ProcessPoolExecutor is typically **not** the best choice
- This exercise helps you understand when **not** to use multiprocessing
- Compare the performance with the threading version

**Example Output:**
```
Fetching 20 TODO items using ProcessPoolExecutor...
TODO 1: delectus aut autem
TODO 2: quis ut nam facilis et officia qui
TODO 4: et porro tempora
...
TODO 20: ullam nobis libero sapiente ad optio sint

Summary:
Total execution time: 1.23 seconds
Average time per request: 0.062 seconds
```


### Part 3: Asyncio with aiohttp Implementation

**Requirements:**
- Create a program named `fetch_todos_asyncio.py`
- Use `asyncio` for concurrency
- Use the `aiohttp` library for HTTP requests (you'll need to install it: `pip install aiohttp`)
- Create an async function `async def fetch_todo(session: aiohttp.ClientSession, todo_id: int) -> dict[str, Any]` that fetches a single TODO item
- Use `asyncio.gather()` to fetch all 20 items concurrently
- Print each TODO title as it's received
- Measure execution time and print summary statistics
- Properly manage the aiohttp ClientSession (use async context manager)

**Example Output:**
```
Fetching 20 TODO items using asyncio and aiohttp...
TODO 2: quis ut nam facilis et officia qui
TODO 1: delectus aut autem
TODO 5: laboriosam mollitia et enim quasi adipisci quia provident illum
TODO 3: fugiat veniam minus
...
TODO 20: ullam nobis libero sapiente ad optio sint

Summary:
Total execution time: 0.42 seconds
Average time per request: 0.021 seconds
```

**Hints:**
- Look at `modules\12_Concurrency\demos\async_download_and_process.py`
- And `modules\12_Concurrency\demos\good_and_bad_async_handlers\good_request_handler.py`

---

## Exercise 2: Performance Improvement of Non-Efficient FastAPI Endpoint

**Description:**
You are given a FastAPI application with a poorly implemented endpoint that performs a mix of CPU-bound and I/O-bound operations inefficiently. Your task is to identify the performance bottlenecks, measure the current performance under load, and refactor the code to significantly improve its throughput using asyncio patterns.

**Learning Objectives:**
- Identify performance anti-patterns in async code
- Understand the difference between CPU-bound and I/O-bound operations
- Learn when to use `asyncio` vs `ProcessPoolExecutor` vs blocking I/O
- Use `run_in_executor()` to integrate blocking operations with asyncio
- Measure API performance under high load
- Refactor synchronous code to use async libraries

---

### Part 1: Analyze and Measure Current Performance

**Given Code: `app.py` (Inefficient Version)**

**Requirements for Part 1:**

1. **Run and Test the Current Implementation:**
   - Save the code above as `app.py`
   - Run the application: `python app.py`
   - Test a single request using curl or browser:
     ```bash
     curl "http://localhost:8000/process_order?user_id=123&product_id=456&zip_code=12345"
     ```
   - Measure how long a single request takes

2. **Create a Load Testing Script:**
   - Create `load_test.py` based on the reference: `modules\12_Concurrency\demos\good_and_bad_async_handlers\highload_simulator.py`
   - Configure it to send 10-20 concurrent requests to your endpoint
   - Measure: total time, average response time, requests per second

3. **Document the Problems:**
   - Create a file `analysis.md` that identifies all performance issues in the code
   - For each problem, explain:
     - What the problem is
     - Why it's a problem (impact on performance)
     - What the correct approach should be
---

### Part 2: Refactor for Performance

**Requirements:**

Create `app_optimized.py` that fixes all the performance issues using the following approaches:

1. **Use AsyncIO for I/O Operations:**
   - Replace blocking sleep operations with async versions using `asyncio.sleep()`
   - Convert all I/O functions to async functions
   - Run independent I/O operations concurrently using `asyncio.gather()`

2. **Use ProcessPoolExecutor for CPU-Bound Work:**
   - Move the Fibonacci calculation to run in a separate process
   - Use `loop.run_in_executor()` with `ProcessPoolExecutor`
   - Reference: `modules\12_Concurrency\demos\async_download_and_process.py`

**In the real world, use Async Libraries Where Possible:**
   - For real I/O operations (not simulated), use async libraries:
     - HTTP requests: Use `aiohttp` instead of `requests`
     - Database queries: Use `aiomysql` for MySQL, `asyncpg` for PostgreSQL, etc.
   - For this exercise, simulated operations with `asyncio.sleep()` are acceptable

### Part 3: Measure and Compare Performance

**Requirements:**

1. **Run Load Tests on Both Versions:**
   - Test the original `app.py` (port 8000)
   - Test the optimized `app_optimized.py` (port 8001)
   - Use the same load test script for both

2. **Compare Results:**
   - Create a file `performance_comparison.md` that documents:
     - Original version metrics (total time, avg response time, requests/second)
     - Optimized version metrics
     - Improvement percentage

3. **Expected Improvements:**
   - Response time should decrease by 50-70%
   - Throughput (requests per second) should increase by 2-3x
   - Under high load, the difference should be even more dramatic

**Example Performance Comparison:**

```
Original Version (app.py):
- Total time: 45.2 seconds
- Average response time: 2.26 seconds
- Requests per second: 0.44

Optimized Version (app_optimized.py):
- Total time: 8.9 seconds
- Average response time: 0.45 seconds
- Requests per second: 2.25

Improvement:
- Response time: 80% faster
- Throughput: 5x more requests per second
```

## Exercise 3: Rewrite the High-Load Simulator with asyncio and aiohttp

**Description:**
In this exercise you will first run the class demo that compares a blocking (bad) FastAPI handler with a non-blocking (good) one, observing the difference in throughput. Then you will rewrite the load-testing script that drives the demo — replacing `concurrent.futures.ThreadPoolExecutor` and `requests` with native `asyncio` and `aiohttp`.

**Learning Objectives:**
- Run and observe a real async vs. blocking FastAPI demo
- Practice replacing thread-based concurrency with coroutine-based concurrency

---

### Part 1: Run the Demo

1. Navigate to `modules/12_Concurrency/demos/good_and_bad_async_handlers/` and read the code to understand what the two FastAPI servers do.
2. Start all servers as we did in the demo
3. Run the existing `highload_simulator.py` script and observe the printed statistics for both the bad handler and the good handler.
4. Note the difference in average response time and requests per second between the two handlers.

---

### Part 2: Rewrite the Simulator with asyncio and aiohttp

Create a new file `highload_simulator_async.py` in the **same demo directory** that is a drop-in replacement for `highload_simulator.py`, but uses `asyncio` and `aiohttp` instead of `requests` and `ThreadPoolExecutor`.

**Requirements:**

- Import `asyncio` and `aiohttp` instead of `requests`, `concurrent.futures`, and `threading`.
- Keep the same constants: `NUM_REQUESTS = 20`, `BAD_HANDLER_URL`, `GOOD_HANDLER_URL` (reuse `constants.py`).
  - Create an async function that sends a GET request using `aiohttp`.
  - Measures and returns the elapsed time for that single request.
  - Prints a per-request line similar to the original (generate id for a task with `uuid`).
- Create an async function `run_load_test(url: str, description: str) -> None` that:
  - Fires `NUM_REQUESTS` concurrent requests using `asyncio.gather()`.
  - Prints the same summary statistics as the original: total time, average, median, max, min, and requests per second.
- The entry point `main()` should be an `async def` and called with `asyncio.run(main())` inside the `if __name__ == "__main__":` guard.
- All functions must have type hints.
- The file must pass `black`, `flake8`, and `mypy` checks.

---

## Submission Structure

Your submission should have the following structure:

```
concurrency_exercises/
├── exercise1_todo_fetching/
│   ├── fetch_todos_threading.py
│   ├── fetch_todos_multiprocessing.py
│   └── fetch_todos_asyncio.py
│
├── exercise2_fastapi_optimization/
│   ├── app.py                         # Original inefficient version
│   ├── app_optimized.py               # Your optimized version
│   ├── load_test.py                   # Load testing script
│   └── performance_comparison.md      # Before/after metrics
│
├── exercise3_async_simulator/
│   └── highload_simulator_async.py    # asyncio + aiohttp rewrite
│
├── requirements.txt                   # Dependencies: requests, aiohttp...
└── .gitignore
```
