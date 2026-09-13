from dataclasses import dataclass


@dataclass
class EvidenceFile:
    """Store metadata collected about one evidence file."""

    name: str
    path: str
    extension: str
    size_bytes: int
    modified_time: float
    sha256: str

@dataclass
class TriageResult:
    """Store security analysis and risk results for one evidence file."""

    evidence_file: EvidenceFile
    ip_addresses: list[str]
    event_counts: dict[str, int]
    risk_score: int
    risk_level: str
    reasons: list[str]