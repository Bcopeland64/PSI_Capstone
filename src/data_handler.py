"""Data persistence layer for the encrypted credential vault (SQLite).

This module isolates every piece of raw SQL and ties it together
with the encryption layer in `security.py`. Callers never see raw
SQL or handle encryption directly -- they only work with
`Credential` objects and a derived key.
"""

import sqlite3
from pathlib import Path

from src.models import Credential
from src.security import SecurityError, decrypt, derive_key, encrypt


class DataHandlerError(Exception):
    """Raised when a database operation fails unexpectedly."""


# A fixed, known plaintext used only to verify the master password on
# unlock. It is stored encrypted; if decrypting it with the supplied
# key succeeds, the master password is correct.
_VERIFIER_PLAINTEXT = "vault-unlock-check"


class VaultDatabase:
    """Wraps all SQLite operations for the credential vault."""

    def __init__(self, db_path: str = "data/vault.db"):
        """Open (or create) the SQLite database and its schema.

        Args:
            db_path: Filesystem path to the SQLite database file.
                Parent directories are created automatically.
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self._create_schema()
        except sqlite3.Error as exc:
            raise DataHandlerError(
                f"Could not open database at '{db_path}': {exc}"
            ) from exc

    def _create_schema(self) -> None:
        """Create the required tables if they do not already exist."""
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS vault_meta (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                salt BLOB NOT NULL,
                verifier BLOB NOT NULL
            );

            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password BLOB NOT NULL
            );
            """
        )
        self.connection.commit()

    def is_initialized(self) -> bool:
        """Check whether a master password has already been set up.

        Returns:
            True if the vault has salt/verifier stored, else False.
        """
        row = self.connection.execute(
            "SELECT id FROM vault_meta WHERE id = 1"
        ).fetchone()
        return row is not None

    def initialize_vault(self, master_password: str) -> bytes:
        """Set up the vault for first use with a chosen master password.

        Args:
            master_password: The master password to protect the vault.

        Returns:
            The derived encryption key, ready for immediate use.

        Raises:
            DataHandlerError: If the vault was already initialized.
        """
        if self.is_initialized():
            raise DataHandlerError("Vault is already initialized.")

        from src.security import generate_salt

        salt = generate_salt()
        key = derive_key(master_password, salt)
        verifier = encrypt(_VERIFIER_PLAINTEXT, key)

        self.connection.execute(
            "INSERT INTO vault_meta (id, salt, verifier) VALUES (1, ?, ?)",
            (salt, verifier),
        )
        self.connection.commit()
        return key

    def unlock(self, master_password: str) -> bytes:
        """Derive and verify the encryption key from the master password.

        Args:
            master_password: The master password entered by the user.

        Returns:
            The derived key, valid for encrypting/decrypting entries.

        Raises:
            DataHandlerError: If the vault has not been initialized.
            SecurityError: If the master password is incorrect.
        """
        row = self.connection.execute(
            "SELECT salt, verifier FROM vault_meta WHERE id = 1"
        ).fetchone()
        if row is None:
            raise DataHandlerError("Vault has not been initialized yet.")

        key = derive_key(master_password, row["salt"])
        # Raises SecurityError if the master password is wrong.
        decrypt(row["verifier"], key)
        return key

    def add_credential(self, credential: Credential, key: bytes) -> int:
        """Encrypt and insert a new credential record.

        Args:
            credential: The Credential to store (entry_id is ignored).
            key: The active vault encryption key.

        Returns:
            The auto-generated id of the new row.

        Raises:
            DataHandlerError: If the insert fails.
        """
        try:
            encrypted_password = encrypt(credential.password, key)
            cursor = self.connection.execute(
                """
                INSERT INTO credentials (service, username, encrypted_password)
                VALUES (?, ?, ?)
                """,
                (credential.service, credential.username, encrypted_password),
            )
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as exc:
            raise DataHandlerError(f"Failed to add credential: {exc}") from exc

    def get_all_credentials(self, key: bytes) -> list[Credential]:
        """Fetch and decrypt every stored credential.

        Args:
            key: The active vault encryption key.

        Returns:
            A list of Credential objects with plaintext passwords.
        """
        rows = self.connection.execute(
            "SELECT * FROM credentials ORDER BY service ASC"
        ).fetchall()
        return [self._row_to_credential(row, key) for row in rows]

    def get_by_service(self, service: str, key: bytes) -> list[Credential]:
        """Fetch credentials matching a service name (case-insensitive).

        Args:
            service: The service name to search for.
            key: The active vault encryption key.

        Returns:
            A list of matching Credential objects.
        """
        rows = self.connection.execute(
            "SELECT * FROM credentials WHERE LOWER(service) = LOWER(?)",
            (service,),
        ).fetchall()
        return [self._row_to_credential(row, key) for row in rows]

    def delete_credential(self, entry_id: int) -> bool:
        """Delete a credential by its id.

        Args:
            entry_id: The id of the record to remove.

        Returns:
            True if a row was deleted, False if no such id existed.
        """
        cursor = self.connection.execute(
            "DELETE FROM credentials WHERE id = ?", (entry_id,)
        )
        self.connection.commit()
        return cursor.rowcount > 0

    @staticmethod
    def _row_to_credential(row: sqlite3.Row, key: bytes) -> Credential:
        """Convert a sqlite3.Row into a Credential with decrypted password.

        Raises:
            SecurityError: If decryption fails (wrong key).
        """
        return Credential(
            entry_id=row["id"],
            service=row["service"],
            username=row["username"],
            password=decrypt(row["encrypted_password"], key),
        )

    def close(self) -> None:
        """Close the underlying database connection."""
        self.connection.close()
