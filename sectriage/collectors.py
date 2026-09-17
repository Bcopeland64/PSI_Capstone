"""Data-gathering classes.

Each collector wraps one of the workshop's three days into a reusable,
testable class with a small public surface:

    ProcessCollector    -> Day 2/3: running processes (psutil, with a
                           subprocess fallback if psutil isn't installed)
    FileSystemCollector -> Day 3: file hashing, recent-file timelines,
                           duplicate-content detection
    LogAnalyzer         -> Day 1: text log parsing, level tallies,
                           IP extraction, failed-login counting
    NetworkAnalyzer     -> Day 2: CSV traffic summaries + optional live
                           HTTP/port checks
"""

from __future__ import annotations

import csv
import os
import re
import socket
import subprocess
import sys
import time
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Set, Tuple

from .exceptions import InvalidTargetError, UnsupportedFormatError
from .models import FileRecord, LogSummary, NetworkSummary, ProcessRecord
from .utils import hash_file, iter_files

_IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_LEVEL_PATTERN = re.compile(r"\b(INFO|WARNING|ERROR|CRITICAL|DEBUG)\b")


class ProcessCollector:
    """Gathers a snapshot of currently running processes."""

    def collect(self, limit: int = 10) -> List[ProcessRecord]:
        """Return up to ``limit`` running processes.

        Prefers ``psutil`` (cross-platform); falls back to shelling out to
        ``ps aux`` (POSIX) or ``tasklist`` (Windows) if psutil isn't
        installed, matching the fallback pattern used throughout the
        workshop notebooks.
        """
        try:
            import psutil  # optional third-party dependency

            records = []
            for proc in psutil.process_iter(["pid", "name"]):
                records.append(ProcessRecord(pid=proc.info.get("pid"), name=proc.info.get("name") or "?"))
                if len(records) >= limit:
                    break
            return records
        except ImportError:
            return self._collect_via_subprocess(limit)

    @staticmethod
    def _collect_via_subprocess(limit: int) -> List[ProcessRecord]:
        """Best-effort process listing with no third-party dependencies."""
        command = ["tasklist"] if sys.platform.startswith("win") else ["ps", "aux"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=5, check=False)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

        lines = result.stdout.splitlines()[1:]  # skip the header row
        records = []
        for line in lines[:limit]:
            parts = line.split()
            if not parts:
                continue
            # `ps aux` col 2 is PID, last column is usually the command name.
            pid = parts[1] if len(parts) > 1 and parts[1].isdigit() else None
            name = parts[-1]
            records.append(ProcessRecord(pid=int(pid) if pid else None, name=name))
        return records


class FileSystemCollector:
    """File-integrity and timeline forensics over a single folder."""

    def scan(self, folder: str) -> List[FileRecord]:
        """Hash and stat every file directly inside ``folder``."""
        records = []
        for path in iter_files(folder):
            stat = os.stat(path)
            records.append(
                FileRecord(
                    name=os.path.basename(path),
                    path=path,
                    size_bytes=stat.st_size,
                    modified_epoch=stat.st_mtime,
                    sha256=hash_file(path),
                )
            )
        return records

    def recent(self, folder: str, window_seconds: int = 600) -> List[Tuple[str, int]]:
        """Return ``(filename, age_seconds)`` for files modified within the window."""
        current_time = time.time()
        recent_files = []
        for path in iter_files(folder):
            age = current_time - os.stat(path).st_mtime
            if age <= window_seconds:
                recent_files.append((os.path.basename(path), int(age)))
        return sorted(recent_files, key=lambda item: item[1])

    def find_duplicates(self, folder: str) -> Dict[str, List[str]]:
        """Group filenames by content hash; keep only groups with 2+ files.

        Two differently named files with the same hash can mean a payload
        was copied or renamed to evade detection -- worth flagging in triage.
        """
        by_hash: Dict[str, List[str]] = defaultdict(list)
        for path in iter_files(folder):
            by_hash[hash_file(path)].append(os.path.basename(path))
        return {digest: names for digest, names in by_hash.items() if len(names) > 1}


class LogAnalyzer:
    """Parses plain-text service/auth logs (Day 1 techniques)."""

    def analyze(self, path: str, failed_login_marker: str = "Failed password") -> LogSummary:
        """Summarize ``path``: level counts, unique IPs, and top failed-login IPs.

        Raises:
            InvalidTargetError: if the log file can't be opened.
        """
        try:
            handle = open(path, "r", encoding="utf-8", errors="replace")
        except (FileNotFoundError, IsADirectoryError, PermissionError) as exc:
            raise InvalidTargetError(f"Could not read log '{path}': {exc}") from exc

        level_counts: Counter = Counter()
        ip_set: Set[str] = set()
        failed_ip_counts: Counter = Counter()
        total_lines = 0

        with handle:
            for line in handle:
                total_lines += 1
                level_match = _LEVEL_PATTERN.search(line)
                if level_match:
                    level_counts[level_match.group(1)] += 1

                ips_in_line = _IP_PATTERN.findall(line)
                ip_set.update(ips_in_line)

                if failed_login_marker in line and ips_in_line:
                    # The offending IP is conventionally the last one on the line
                    # (e.g. "Failed password for root from 45.33.12.9").
                    failed_ip_counts[ips_in_line[-1]] += 1

        return LogSummary(
            source=path,
            total_lines=total_lines,
            level_counts=dict(level_counts),
            unique_ips=sorted(ip_set),
            top_offenders=failed_ip_counts.most_common(5),
        )

    def write_filtered(self, in_path: str, out_path: str, keyword: str) -> int:
        """Write only lines containing ``keyword`` from ``in_path`` to ``out_path``.

        Returns the number of lines written.
        """
        try:
            with open(in_path, "r", encoding="utf-8", errors="replace") as src:
                matching = [line for line in src if keyword in line]
        except (FileNotFoundError, IsADirectoryError, PermissionError) as exc:
            raise InvalidTargetError(f"Could not read log '{in_path}': {exc}") from exc

        with open(out_path, "w", encoding="utf-8") as dst:
            dst.writelines(matching)
        return len(matching)


class NetworkAnalyzer:
    """CSV traffic summaries and optional live network checks (Day 2 techniques)."""

    REQUIRED_COLUMNS = {"timestamp", "src_ip", "dst_port", "protocol", "bytes"}

    def analyze_csv(self, path: str, suspicious_ports: Optional[Set[str]] = None) -> NetworkSummary:
        """Summarize a connections/traffic CSV: top ports, top talkers, flagged rows."""
        suspicious_ports = suspicious_ports or {"4444", "31337"}

        try:
            handle = open(path, newline="", encoding="utf-8")
        except (FileNotFoundError, IsADirectoryError, PermissionError) as exc:
            raise InvalidTargetError(f"Could not read CSV '{path}': {exc}") from exc

        with handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None or not self.REQUIRED_COLUMNS.issubset(reader.fieldnames):
                raise UnsupportedFormatError(
                    f"'{path}' is missing required columns: {sorted(self.REQUIRED_COLUMNS)}"
                )

            port_counts: Counter = Counter()
            bytes_by_src: Counter = Counter()
            suspicious_hits: List[dict] = []
            total_rows = 0

            for row in reader:
                total_rows += 1
                port_counts[row["dst_port"]] += 1
                try:
                    bytes_by_src[row["src_ip"]] += int(row["bytes"])
                except ValueError:
                    pass  # skip rows with a non-numeric byte count rather than crash
                if row["dst_port"] in suspicious_ports:
                    suspicious_hits.append(dict(row))

        return NetworkSummary(
            source=path,
            total_rows=total_rows,
            top_ports=port_counts.most_common(5),
            top_talkers_by_bytes=bytes_by_src.most_common(5),
            suspicious_hits=suspicious_hits,
        )

    def check_endpoints(self, urls: List[str], timeout: float = 5.0) -> List[Tuple[str, str]]:
        """Hit each URL and report its status code, or an error string.

        Requires the optional `requests` package; degrades to an explanatory
        error entry per URL if it isn't installed.
        """
        try:
            import requests
        except ImportError:
            return [(url, "requests not installed") for url in urls]

        results = []
        for url in urls:
            try:
                response = requests.get(url, timeout=timeout)
                results.append((url, str(response.status_code)))
            except requests.RequestException as exc:
                results.append((url, f"error: {exc}"))
        return results

    def check_port(self, host: str, port: int, timeout: float = 0.5, allow_remote: bool = False) -> str:
        """Check whether ``port`` is open on ``host``.

        Safety: by default only ``localhost``/``127.0.0.1`` may be scanned,
        matching the "authorized targets only" rule from the workshop's
        ethics briefing. Pass ``allow_remote=True`` to override for a host
        you are explicitly authorized to test.
        """
        if not allow_remote and host not in {"localhost", "127.0.0.1"}:
            raise InvalidTargetError(
                f"Refusing to scan '{host}': only localhost is scanned by default. "
                "Pass allow_remote=True only for hosts you are authorized to test."
            )
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
            return "open" if result == 0 else "closed"
        except socket.gaierror as exc:
            raise InvalidTargetError(f"Could not resolve host '{host}': {exc}") from exc
