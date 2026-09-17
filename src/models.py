"""
models.py
---------
Plain-data classes shared across the SentryTriage toolkit.

Keeping these in one module gives every other module (logic, data_handler,
main) a single, typed vocabulary to pass around instead of loose dicts and
tuples.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Connection:
    """A single row from a network-connection log (e.g. a firewall/NetFlow export)."""

    timestamp: str
    src_ip: str
    dst_port: int
    protocol: str
    num_bytes: int

    @classmethod
    def from_row(cls, row: dict) -> "Connection":
        """Build a Connection from a csv.DictReader row, validating/coercing types.

        Raises:
            ValueError: if dst_port or bytes cannot be parsed as integers.
        """
        try:
            dst_port = int(row["dst_port"])
            num_bytes = int(row["bytes"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Malformed connection row {row!r}: {exc}") from exc

        return cls(
            timestamp=row.get("timestamp", ""),
            src_ip=row.get("src_ip", ""),
            dst_port=dst_port,
            protocol=row.get("protocol", "unknown"),
            num_bytes=num_bytes,
        )


@dataclass
class FileArtifact:
    """Metadata + hash for one file discovered during a filesystem scan."""

    name: str
    path: str
    size_bytes: int
    modified_epoch: float
    sha256: str

    @property
    def modified_iso(self) -> str:
        """Human-readable modified time, ISO-ish, for reports."""
        return datetime.fromtimestamp(self.modified_epoch).strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class PortResult:
    """Result of probing a single TCP port on a host."""

    host: str
    port: int
    is_open: bool


@dataclass
class TriageReport:
    """Aggregated results of one full triage run, ready for persistence/printing."""

    generated_at: str
    target: str
    protocol_counts: dict = field(default_factory=dict)
    watchlist_hits: List[dict] = field(default_factory=list)
    top_talker: Optional[dict] = None
    recent_files: List[dict] = field(default_factory=list)
    duplicate_groups: List[List[str]] = field(default_factory=list)
    open_ports: List[int] = field(default_factory=list)
    process_count: Optional[int] = None
    notes: List[str] = field(default_factory=list)
