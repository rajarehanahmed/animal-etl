import logging
from typing import Any

import requests
from tenacity import before_sleep_log, retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class APIClient:
    timeout_seconds = 30

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    # retry the request if it fails, after a random exponential backoff, raise the last exception if all retries fail
    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        # keep the timeout to 30 to be on safe side, server might take time to process, but timeout after 30 seconds
        # so that the client does not hang indefinitely
        response = self.session.get(url, params=params, timeout=self.timeout_seconds)

        response.raise_for_status()
        return response.json()

    @retry(
        wait=wait_exponential(min=1, max=10),
        stop=stop_after_attempt(5),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def post(self, endpoint: str, data: list[dict[str, Any]]) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        # timeout for the same reason as in get
        response = self.session.post(url, json=data, timeout=self.timeout_seconds)

        response.raise_for_status()

        return response.json()
