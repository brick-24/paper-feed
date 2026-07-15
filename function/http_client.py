"""Shared HTTP client with retry logic and timeout configuration."""

from __future__ import annotations

import logging
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# Default timeout for all requests (connect, read)
DEFAULT_TIMEOUT = (5, 10)  # (connect_timeout, read_timeout)

# Retry configuration
RETRY_CONFIG = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],
    raise_on_status=False,
)


def create_session(retry_config: Retry | None = RETRY_CONFIG) -> requests.Session:
    """Create a requests Session with configured retry strategy.

    Args:
        retry_config: urllib3 Retry configuration. None disables retries.

    Returns:
        Configured requests.Session instance.
    """
    session = requests.Session()

    if retry_config:
        adapter = HTTPAdapter(max_retries=retry_config)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

    return session


# Default shared session for simple use cases
_DEFAULT_SESSION: requests.Session | None = None


def get_default_session() -> requests.Session:
    """Get or create the default shared session."""
    global _DEFAULT_SESSION
    if _DEFAULT_SESSION is None:
        _DEFAULT_SESSION = create_session()
    return _DEFAULT_SESSION


def get_json(
    url: str,
    params: dict[str, Any] | None = None,
    *,
    timeout: tuple[float, float] = DEFAULT_TIMEOUT,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """GET request expecting JSON response with retry logic.

    Args:
        url: Request URL.
        params: Query parameters.
        timeout: (connect, read) timeout tuple.
        session: Optional custom session. Uses default session if not provided.

    Returns:
        Parsed JSON response.

    Raises:
        requests.HTTPError: On non-2xx response after retries.
        requests.Timeout: On timeout.
        ValueError: If response is not valid JSON.
    """
    sess = session or get_default_session()
    resp = sess.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_text(
    url: str,
    params: dict[str, Any] | None = None,
    *,
    timeout: tuple[float, float] = DEFAULT_TIMEOUT,
    session: requests.Session | None = None,
) -> str:
    """GET request expecting text response with retry logic."""
    sess = session or get_default_session()
    resp = sess.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def get_content(
    url: str,
    params: dict[str, Any] | None = None,
    *,
    timeout: tuple[float, float] = DEFAULT_TIMEOUT,
    session: requests.Session | None = None,
) -> bytes:
    """GET request returning raw content (for images, etc.) with retry logic."""
    sess = session or get_default_session()
    resp = sess.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.content