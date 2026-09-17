"""Custom exceptions used throughout SecTriage.

Using a small, specific exception hierarchy (instead of letting raw
``OSError`` / ``KeyError`` etc. bubble up) lets the CLI layer catch one
base class and print a clean, analyst-friendly message instead of a
Python traceback.
"""


class TriageError(Exception):
    """Base class for all SecTriage errors."""


class InvalidTargetError(TriageError):
    """Raised when a required file or folder is missing or the wrong type."""


class UnsupportedFormatError(TriageError):
    """Raised when an input file exists but its contents are malformed."""


class PersistenceError(TriageError):
    """Raised when saving/loading a report (JSON, CSV, or SQLite) fails."""
