from typing import Any

import requests

API_BASE_URL = "http://localhost:8000"
HTTP_OK = 200


def request_json(
    method: str,
    path: str,
    params: dict[str, Any] | None = None,
) -> Any | None:
    """Perform an HTTP request and return parsed JSON (or None on error)."""
    try:

        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            params=params,
        )

    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Is the server running?")
        return None

    if not response.ok:
        print(f"API error ({response.status_code})")
        print(response.text)
        return None
    if not response.text.strip():
        return {}

    try:
        data = response.json()
    except ValueError:
        print("Invalid response from API")
        return None
    return data


def request_and_print(
    method: str,
    path: str,
    success_message: str,
    params: dict[str, Any] | None = None,
) -> Any:
    """
    Call the API and print a success message only if the request succeeded.

    We keep printing decisions here so UI methods stay short and readable.
    """
    data = request_json(
        method,
        path,
        params=params,
    )
    if data is None:
        return None

    print(success_message)
    return data
