## Performance Comparison

### Original Version (`app.py`)
- Total test duration: **33.00 seconds**
- Average response time: **18.249 seconds**
- Throughput: **0.61 requests/second**

### Optimized Version (`app_optimized.py`)
- Total test duration: **4.13 seconds**
- Average response time: **3.936 seconds**
- Throughput: **4.84 requests/second**

---

## Performance Improvements

- **Response time reduced by 78.4%**
- **Throughput increased by 7.9×** (≈693% increase)

---

### Summary

The optimized version significantly improves performance by:
- Running independent I/O operations concurrently using `asyncio.gather()`
- Offloading CPU-bound Fibonacci calculations to a `ProcessPoolExecutor`
- Eliminating blocking calls that previously stalled the event loop

Under higher concurrency, the performance gap becomes even more dramatic due to improved parallelism and reduced blocking behavior.