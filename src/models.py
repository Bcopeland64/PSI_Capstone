from dataclasses import dataclass

@dataclass
class FileEvidence:
    """Store information about one evidence file."""
    name: str
    size: int
    modified_time: float
    sha256: str
    recent: bool = False

@dataclass
class ProcessInfo:
    """Store basic information about a running process."""
    pid: int
    name: str
