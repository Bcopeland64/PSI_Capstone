"""
logic.py
--------
Core analysis functions for the SentryTriage toolkit. Each function takes
plain inputs (a list of Connections, a folder path, etc.) and returns plain
data (dicts/lists/dataclasses) -- no printing, no file writes. That keeps
this module easy to unit test and reusable from both the CLI and, e.g., a
future web UI.
"""

import os
import socket
import subprocess
import time
from collections import Counter
from datetime import datetime
from typing import List, Optional

import requests

from src.models import Connection, FileArtifact, PortResult, TriageReport
from src.utils import hash_file, validate_host, validate_port


# ---------------------------------------------------------------------------
# Network log analysis
# ---------------------------------------------------------------------------

def count_protocols(connections: List[Connection]) -> Counter:
    """Tally how many connections use each protocol (tcp/udp/etc.)."""
    return Counter(c.protocol for c in connections)


def find_watchlist_hits(connections: List[Connection], watchlist_ports: List[int]) -> List[dict]:
    """Return every connection whose destination port is on the watchlist."""
    watch = set(watchlist_ports)
    hits = []
    for c in connections:
        if c.dst_port in watch:
            hits.append(
                {
                    "timestamp": c.timestamp,
                    "src_ip": c.src_ip,
                    "dst_port": c.dst_port,
                    "protocol": c.protocol,
                    "bytes": c.num_bytes,
                }
            )
    return hits


def find_top_talker(connections: List[Connection]) -> Optional[dict]:
    """Return the src_ip with the highest *total* bytes transferred, or None if empty."""
    if not connections:
        return None
    totals: Counter = Counter()
    for c in connections:
        totals[c.src_ip] += c.num_bytes
    src_ip, total_bytes = totals.most_common(1)[0]
    return {"src_ip": src_ip, "total_bytes": total_bytes}


def check_ip_reputation(ip: str, timeout: float = 3.0) -> dict:
    """Look up coarse geolocation/ASN info for an IP via a public HTTP API.

    This is the toolkit's external API integration: a real analyst uses a
    quick reputation/geolocation check to help decide whether a watchlist hit
    is worth escalating (e.g. traffic to an unexpected country). Network
    calls are unreliable in a CLI tool, so failures are caught and reported
    as 'unknown' rather than crashing the scan.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return {
            "ip": ip,
            "country": data.get("country", "unknown"),
            "isp": data.get("isp", "unknown"),
            "status": data.get("status", "unknown"),
        }
    except requests.RequestException as exc:
        return {"ip": ip, "country": "unknown", "isp": "unknown", "status": f"lookup_failed: {exc}"}


# ---------------------------------------------------------------------------
# Filesystem / evidence scanning
# ---------------------------------------------------------------------------

def scan_folder(folder: str) -> List[FileArtifact]:
    """Hash and stat every file directly inside `folder`, returning FileArtifacts."""
    artifacts = []
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            continue
        stat_result = os.stat(path)
        artifacts.append(
            FileArtifact(
                name=name,
                path=path,
                size_bytes=stat_result.st_size,
                modified_epoch=stat_result.st_mtime,
                sha256=hash_file(path),
            )
        )
    return artifacts


def build_timeline(artifacts: List[FileArtifact]) -> List[FileArtifact]:
    """Return artifacts sorted chronologically by modified time."""
    return sorted(artifacts, key=lambda a: a.modified_epoch)


def flag_recent_files(artifacts: List[FileArtifact], window_seconds: int, now: Optional[float] = None) -> List[dict]:
    """Return artifacts modified within `window_seconds` of `now` (default: current time)."""
    now = now if now is not None else time.time()
    recent = []
    for a in artifacts:
        age = now - a.modified_epoch
        if 0 <= age <= window_seconds:
            recent.append({"name": a.name, "age_seconds": int(age), "sha256": a.sha256[:12]})
    return recent


def find_duplicates(artifacts: List[FileArtifact]) -> List[List[str]]:
    """Group filenames that share an identical SHA-256 hash (potential renamed payloads)."""
    by_hash = {}
    for a in artifacts:
        by_hash.setdefault(a.sha256, []).append(a.name)
    return [names for names in by_hash.values() if len(names) > 1]


# ---------------------------------------------------------------------------
# Port scanning
# ---------------------------------------------------------------------------

def check_port(host: str, port: int, timeout: float = 0.5) -> PortResult:
    """Attempt a TCP connect to (host, port); return a PortResult (open/closed)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((host, port))
    finally:
        sock.close()
    return PortResult(host=host, port=port, is_open=(result == 0))


def scan_port_range(host: str, start_port: int, end_port: int) -> List[PortResult]:
    """Validate inputs and scan every port in [start_port, end_port] on host."""
    host = validate_host(host)
    start_port = validate_port(start_port)
    end_port = validate_port(end_port)
    if start_port > end_port:
        raise ValueError(f"start_port ({start_port}) must be <= end_port ({end_port})")
    return [check_port(host, p) for p in range(start_port, end_port + 1)]


# ---------------------------------------------------------------------------
# Process listing
# ---------------------------------------------------------------------------

def list_processes(limit: int = 20) -> List[dict]:
    """List running processes, preferring psutil but falling back to `ps aux`.

    The fallback keeps the tool usable in minimal/CI environments where
    psutil isn't installed, satisfying the "handle missing optional
    dependency" requirement gracefully instead of crashing.
    """
    try:
        import psutil  # optional third-party dependency

        procs = []
        for p in psutil.process_iter(["pid", "name"]):
            procs.append(p.info)
            if len(procs) >= limit:
                break
        return procs
    except ImportError:
        try:
            output = subprocess.run(
                ["ps", "aux"], capture_output=True, text=True, timeout=5, check=True
            ).stdout
            lines = output.strip().splitlines()[1 : limit + 1]
            return [{"raw": line} for line in lines]
        except (subprocess.SubprocessError, FileNotFoundError, OSError) as exc:
            return [{"error": f"process listing unavailable: {exc}"}]


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def build_report(
    target: str,
    connections: Optional[List[Connection]] = None,
    watchlist_ports: Optional[List[int]] = None,
    artifacts: Optional[List[FileArtifact]] = None,
    recent_window_seconds: int = 3600,
    port_results: Optional[List[PortResult]] = None,
    process_count: Optional[int] = None,
) -> TriageReport:
    """Assemble a full TriageReport from whichever pieces of data are available.

    Every argument is optional so callers can run a partial triage (e.g. just
    a log scan, or just a file scan) and still get a well-formed report.
    """
    report = TriageReport(generated_at=datetime.now().isoformat(timespec="seconds"), target=target)

    if connections is not None:
        report.protocol_counts = dict(count_protocols(connections))
        report.watchlist_hits = find_watchlist_hits(connections, watchlist_ports or [])
        report.top_talker = find_top_talker(connections)

    if artifacts is not None:
        timeline = build_timeline(artifacts)
        report.recent_files = flag_recent_files(timeline, recent_window_seconds)
        report.duplicate_groups = find_duplicates(timeline)

    if port_results is not None:
        report.open_ports = [r.port for r in port_results if r.is_open]

    if process_count is not None:
        report.process_count = process_count

    if not any([connections, artifacts, port_results, process_count]):
        report.notes.append("No data sources were provided to this triage run.")

    return report
