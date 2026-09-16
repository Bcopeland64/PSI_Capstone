"""
utils.py
--------
Helper functions used across the project: URL/input validation,
resilient HTTP requests (with retry/back-off for rate limiting),
and file hashing (SHA-256), following the security-log-analysis
patterns introduced in the workshop (Day 1: validation + regex,
Day 2: requests + hashlib, Day 3: file metadata).
"""

import hashlib
import os
import time
from urllib.parse import urlparse

import requests


def validate_url(url: str) -> str:
    """
    Validate that `url` is a well-formed http(s) URL.

    Raises:
        ValueError: if the URL is empty, malformed, or uses an
            unsupported scheme (only http/https are accepted).

    Returns:
        The cleaned (stripped) URL string.
    """
    if not url or not url.strip():
        raise ValueError("The URL cannot be empty.")

    cleaned = url.strip()
    parsed = urlparse(cleaned)

    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Unsupported URL scheme '{parsed.scheme}'. Use http:// or https://."
        )
    if not parsed.netloc:
        raise ValueError(f"'{url}' is not a valid URL (missing host).")

    return cleaned


def ensure_directory(path: str) -> None:
    """Create `path` (and parents) if it doesn't already exist."""
    os.makedirs(path, exist_ok=True)


def safe_request(url: str, timeout: float = 10.0, retries: int = 3,
                  backoff_seconds: float = 1.5):
    """
    Perform a GET request with basic error handling and retry/back-off,
    mirroring the "flag anything that isn't 200" technique from Day 2
    but adding resilience for timeouts, connection errors and HTTP 429
    (rate limiting).

    Returns:
        requests.Response on success, or None if every attempt failed.
    """
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                url,
                timeout=timeout,
                headers={"User-Agent": "CapstoneEthicalScraper/1.0"},
            )

            if response.status_code == 429:
                # Rate limited: respect Retry-After if present, else back off.
                wait = float(response.headers.get("Retry-After", backoff_seconds * attempt))
                print(f"[!] Rate limited (429). Waiting {wait:.1f}s before retry...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            return response

        except requests.exceptions.Timeout as exc:
            last_error = exc
            print(f"[!] Attempt {attempt}/{retries}: request timed out.")
        except requests.exceptions.ConnectionError as exc:
            last_error = exc
            print(f"[!] Attempt {attempt}/{retries}: connection error.")
        except requests.exceptions.HTTPError as exc:
            # Non-recoverable HTTP error (404, 500, etc.) -- no point retrying.
            print(f"[!] HTTP error: {exc}")
            return None
        except requests.exceptions.RequestException as exc:
            last_error = exc
            print(f"[!] Attempt {attempt}/{retries}: request failed ({exc}).")

        if attempt < retries:
            time.sleep(backoff_seconds * attempt)

    print(f"[x] All {retries} attempts failed for '{url}'. Last error: {last_error}")
    return None


def compute_sha256(file_path: str) -> str:
    """
    Compute the SHA-256 hash of a file's contents (Day 2/Day 3 technique),
    used here to fingerprint saved reports for integrity checking.

    Raises:
        FileNotFoundError: if `file_path` does not exist.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")

    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def prompt_nonempty(prompt_text: str) -> str:
    """Prompt the user until a non-empty string is entered."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")
