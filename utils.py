

"""Utility module providing input validation and file existence checks."""

import os


def validate_host(host: str) -> bool:
  """Validate if the provided host string is non-empty."""
  return bool(host and isinstance(host, str))


def file_exists(path: str) -> bool:
  """Check if a file exists on the filesystem."""
  return os.path.exists(path)