import uvicorn

from solution.api.main import app

PORT = 8000
KEEP_ALIVE_TIMEOUT = 65

uvicorn.run(
    app,
    host="127.0.0.1",
    port=PORT,
    log_level="info",
    timeout_keep_alive=KEEP_ALIVE_TIMEOUT,
    access_log=True,
    proxy_headers=True,
)

