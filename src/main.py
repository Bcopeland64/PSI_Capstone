"""Main entry point for the Password Vault CLI application.

Run with:
    python -m src.main

This module wires together the data layer (data_handler), the
encryption/analysis layer (security), and validation (utils) behind
a simple text menu. It uses the `rich` library for nicer terminal
output, but degrades gracefully to plain `print` if `rich` is
unavailable.
"""

import getpass
import sys

from src.data_handler import DataHandlerError, VaultDatabase
from src.logic import export_report_to_csv, vault_health_report
from src.models import Credential
from src.security import SecurityError, analyze_strength, generate_strong_password
from src.utils import (
    ValidationError,
    validate_master_password,
    validate_password,
    validate_positive_int,
    validate_service,
    validate_username,
)

try:
    from rich.console import Console
    from rich.table import Table

    _console = Console()
    _RICH_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised only without rich installed
    _RICH_AVAILABLE = False
    _console = None


MENU_TEXT = """
========== Password Vault ==========
1. Add credential
2. List all credentials (reveal passwords)
3. Look up by service
4. Vault health report
5. Generate a strong password
6. Export security summary to CSV (no passwords included)
7. Delete a credential
8. Exit
======================================
"""


def prompt_master_password(prompt: str = "Master password: ") -> str:
    """Prompt for a master password without echoing it to the terminal.

    Falls back to a visible `input()` only if the terminal does not
    support hidden input (e.g. some non-interactive test runners).

    Args:
        prompt: The prompt text to display.

    Returns:
        The entered master password.
    """
    try:
        return getpass.getpass(prompt)
    except Exception:  # pragma: no cover - depends on terminal environment
        return input(prompt)


def unlock_or_initialize_vault(db: VaultDatabase) -> bytes:
    """Set up a new vault or unlock an existing one.

    Args:
        db: An open VaultDatabase instance.

    Returns:
        The derived encryption key for this session.

    Raises:
        SystemExit: If setup/unlock ultimately fails.
    """
    if not db.is_initialized():
        print("No vault found. Let's create one.")
        while True:
            try:
                raw = prompt_master_password("Choose a master password: ")
                master_password = validate_master_password(raw)
                confirm = prompt_master_password("Confirm master password: ")
                if confirm != master_password:
                    print("Passwords do not match. Try again.")
                    continue
                return db.initialize_vault(master_password)
            except ValidationError as exc:
                print(f"Input error: {exc}")

    for attempt in range(3):
        raw = prompt_master_password("Master password: ")
        try:
            return db.unlock(raw)
        except SecurityError as exc:
            print(f"{exc} ({2 - attempt} attempt(s) left)")

    print("Too many failed attempts. Exiting.")
    sys.exit(1)


def print_credentials(credentials: list[Credential]) -> None:
    """Print a list of credentials as a table (rich) or plain lines.

    Args:
        credentials: The credentials to display, with passwords
            already decrypted.
    """
    if not credentials:
        print("No credentials to display.")
        return

    if _RICH_AVAILABLE:
        table = Table(title="Credentials")
        table.add_column("ID", justify="right")
        table.add_column("Service")
        table.add_column("Username")
        table.add_column("Password")
        table.add_column("Strength")

        for credential in credentials:
            result = analyze_strength(credential.password)
            table.add_row(
                str(credential.entry_id),
                credential.service,
                credential.username,
                credential.password,
                f"{result['rating']} ({result['score']})",
            )
        _console.print(table)
    else:
        for credential in credentials:
            result = analyze_strength(credential.password)
            print(f"{credential} | password: {credential.password} "
                  f"| strength: {result['rating']}")


def handle_add(db: VaultDatabase, key: bytes) -> None:
    """Handle the 'add credential' menu option."""
    try:
        service = validate_service(input("Service (e.g. GitHub): "))
        username = validate_username(input("Username/email: "))
        raw_password = prompt_master_password("Password (hidden): ")
        password = validate_password(raw_password)
    except ValidationError as exc:
        print(f"Input error: {exc}")
        return

    result = analyze_strength(password)
    print(f"Strength: {result['rating']} ({result['score']}/100)")
    for issue in result["issues"]:
        print(f"  - {issue}")

    credential = Credential(service=service, username=username, password=password)
    try:
        new_id = db.add_credential(credential, key)
        print(f"Credential saved with id {new_id}.")
    except DataHandlerError as exc:
        print(f"Could not save credential: {exc}")


def handle_list(db: VaultDatabase, key: bytes) -> None:
    """Handle the 'list all credentials' menu option."""
    print_credentials(db.get_all_credentials(key))


def handle_lookup(db: VaultDatabase, key: bytes) -> None:
    """Handle the 'look up by service' menu option."""
    try:
        service = validate_service(input("Service to search for: "))
    except ValidationError as exc:
        print(f"Input error: {exc}")
        return

    print_credentials(db.get_by_service(service, key))


def handle_report(db: VaultDatabase, key: bytes) -> None:
    """Handle the 'vault health report' menu option."""
    print(vault_health_report(db.get_all_credentials(key)))


def handle_generate(_db: VaultDatabase, _key: bytes) -> None:
    """Handle the 'generate a strong password' menu option."""
    try:
        raw_length = input("Length (default 16): ").strip() or "16"
        length = validate_positive_int(raw_length, field_name="length")
    except ValidationError as exc:
        print(f"Input error: {exc}")
        return

    password = generate_strong_password(length)
    print(f"Generated password: {password}")


def handle_export(db: VaultDatabase, key: bytes) -> None:
    """Handle the 'export security summary' menu option."""
    output_path = input("Output CSV path (e.g. data/report.csv): ").strip()
    if not output_path:
        output_path = "data/report.csv"

    try:
        count = export_report_to_csv(db.get_all_credentials(key), output_path)
        print(f"Exported summary for {count} credential(s) to '{output_path}'.")
        print("Note: passwords are never included in exported reports.")
    except OSError as exc:
        print(f"Could not write CSV file: {exc}")


def handle_delete(db: VaultDatabase, _key: bytes) -> None:
    """Handle the 'delete a credential' menu option."""
    raw_id = input("ID of the credential to delete: ").strip()
    try:
        entry_id = validate_positive_int(raw_id, field_name="id")
    except ValidationError as exc:
        print(f"Input error: {exc}")
        return

    if db.delete_credential(entry_id):
        print(f"Credential {entry_id} deleted.")
    else:
        print(f"No credential found with id {entry_id}.")


def run(db: VaultDatabase, key: bytes) -> None:
    """Run the main interactive menu loop.

    Args:
        db: An open, unlocked VaultDatabase instance.
        key: The derived encryption key for this session.
    """
    handlers = {
        "1": handle_add,
        "2": handle_list,
        "3": handle_lookup,
        "4": handle_report,
        "5": handle_generate,
        "6": handle_export,
        "7": handle_delete,
    }

    while True:
        print(MENU_TEXT)
        choice = input("Choose an option (1-8): ").strip()

        if choice == "8":
            print("Vault locked. Goodbye!")
            break

        handler = handlers.get(choice)
        if handler is None:
            print("Invalid option, please choose 1-8.")
            continue

        handler(db, key)


def main() -> None:
    """Application entry point: opens the DB, unlocks it, and starts the menu."""
    try:
        db = VaultDatabase("data/vault.db")
    except DataHandlerError as exc:
        print(f"Fatal error: {exc}")
        sys.exit(1)

    try:
        key = unlock_or_initialize_vault(db)
        run(db, key)
    except KeyboardInterrupt:
        print("\nInterrupted. Vault locked. Goodbye!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
