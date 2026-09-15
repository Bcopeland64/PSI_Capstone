

"""Core triage engine implementing network probing, metadata, and hashing."""

import datetime
import hashlib
import json
import os
import socket
from typing import Any, Dict, List


class TriageScanner:

  """OOP Engine responsible for performing triage investigations on systems and files."""

  def __init__(self, target_host: str = "127.0.0.1"):
    self.target_host = target_host

  def check_port(self, port: int) -> bool:
    """Audit single TCP port state via non-blocking socket connect_ex."""
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(1.0)
      res = s.connect_ex((self.target_host, port))
      s.close()
      return res == 0
    except Exception:
      return False

  def audit_file(self, file_path: str) -> Dict[str, Any]:
    """Retrieve POSIX inode metadata and compute chunked SHA-256 hash."""
    if not os.path.exists(file_path):
      raise FileNotFoundError(f"Target artifact '{file_path}' not found.")

    stats = os.stat(file_path)
    hasher = hashlib.sha256()

    with open(file_path, "rb") as f:
      while chunk := f.read(4096):
        hasher.update(chunk)

    return {
        "file_path": file_path,
        "size_bytes": stats.st_size,
        "last_modified": str(
            datetime.datetime.fromtimestamp(stats.st_mtime)
        ),
        "sha256_hash": hasher.hexdigest(),
    }

  def save_report(self, data: Dict[str, Any], output_path: str) -> None:
    """Persist triage results to JSON storage (Data Persistence)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=4)