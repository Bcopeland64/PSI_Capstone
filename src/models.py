"""Data models for the Password Vault application.

Keeping the model isolated from encryption, storage, and CLI logic
keeps the codebase modular and easy to test.
"""

from dataclasses import dataclass


@dataclass
class Credential:
    """Represents a single stored credential entry.

    The `password` field is only ever held in plaintext in memory
    briefly, right before encryption or right after decryption. It
    is never written to disk in plaintext.

    Attributes:
        entry_id: Unique identifier assigned by the database (None
            until the record has been persisted).
        service: Name of the service/site the credential belongs to
            (e.g. "GitHub", "Email").
        username: The username or email associated with the account.
        password: The plaintext password (only held in memory).
    """

    service: str
    username: str
    password: str
    entry_id: int | None = None

    def __str__(self) -> str:
        """Human-readable representation that never prints the password."""
        return f"[{self.entry_id}] {self.service:<20} | {self.username}"
