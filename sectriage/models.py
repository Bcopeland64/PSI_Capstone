"""Data models for SecTriage.

Plain ``dataclasses`` are used instead of dicts scattered everywhere: they
give every record a fixed shape, IDE/type-checker support, and one place
(``to_dict``) that defines how a record is serialized to JSON.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple


@dataclass
class ProcessRecord:
    """One running process, as reported by psutil or a `ps`/`tasklist` fallback."""

    pid: Optional[int]
    name: str


@dataclass
class FileRecord:
    """Metadata + integrity hash for a single file on disk."""

    name: str
    path: str
    size_bytes: int
    modified_epoch: float
    sha256: str


@dataclass
class LogSummary:
    """Result of running LogAnalyzer over one log file."""

    source: str
    total_lines: int
    level_counts: Dict[str, int] = field(default_factory=dict)
    unique_ips: List[str] = field(default_factory=list)
    top_offenders: List[Tuple[str, int]] = field(default_factory=list)  # (ip, failed_count)


@dataclass
class NetworkSummary:
    """Result of running NetworkAnalyzer over one traffic CSV."""

    source: str
    total_rows: int
    top_ports: List[Tuple[str, int]] = field(default_factory=list)  # (port, connection_count)
    top_talkers_by_bytes: List[Tuple[str, int]] = field(default_factory=list)  # (src_ip, bytes)
    suspicious_hits: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class TriageReport:
    """The combined output of a full triage run against one target folder."""

    target: str
    generated_at: str
    processes: List[ProcessRecord] = field(default_factory=list)
    recent_files: List[Tuple[str, int]] = field(default_factory=list)  # (name, age_seconds)
    file_hashes: List[FileRecord] = field(default_factory=list)
    duplicate_groups: Dict[str, List[str]] = field(default_factory=dict)
    log_summary: Optional[LogSummary] = None
    network_summary: Optional[NetworkSummary] = None

    def to_dict(self) -> dict:
        """Serialize the full report (including nested dataclasses) to a plain dict."""
        return asdict(self)
