"""Business logic: vault health reports and password reuse detection.

This module contains pure/near-pure functions that operate on lists
of `Credential` objects. It has no knowledge of SQLite, encryption
internals, or the CLI -- that separation is what makes it easy to
unit test.

Security note: reports intentionally never print or export
plaintext passwords -- only metadata (service, username, strength
rating) is ever surfaced outside the vault.
"""

import csv
from collections import defaultdict

from src.models import Credential
from src.security import analyze_strength


def find_reused_passwords(credentials: list[Credential]) -> dict[str, list[str]]:
    """Detect passwords reused across more than one service.

    Args:
        credentials: The credentials to check.

    Returns:
        A dict mapping each reused password's services list, keyed
        by an opaque label (never the password itself) -- e.g.
        {"Reused password #1": ["GitHub", "Email"]}. Only groups
        with 2+ services are included.
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for credential in credentials:
        groups[credential.password].append(credential.service)

    reused = {
        f"Reused password #{i + 1}": services
        for i, (_password, services) in enumerate(
            (pw, svcs) for pw, svcs in groups.items() if len(svcs) > 1
        )
    }
    return reused


def vault_health_report(credentials: list[Credential]) -> str:
    """Build a human-readable security health summary of the vault.

    Args:
        credentials: The credentials to analyze.

    Returns:
        A multi-line string report. Never includes plaintext
        passwords.
    """
    if not credentials:
        return "Vault is empty -- no credentials to analyze."

    scores = [analyze_strength(c.password)["score"] for c in credentials]
    ratings = [analyze_strength(c.password)["rating"] for c in credentials]
    weak_count = sum(1 for r in ratings if r in ("Weak", "Fair"))
    average_score = round(sum(scores) / len(scores), 1)

    lines = [
        "=== Vault Health Report ===",
        f"Total credentials     : {len(credentials)}",
        f"Average strength score: {average_score}/100",
        f"Weak/Fair passwords   : {weak_count}",
        "",
        "-- Per-entry strength --",
    ]
    for credential in credentials:
        result = analyze_strength(credential.password)
        lines.append(
            f"  {credential.service:<20}: {result['rating']:<12} "
            f"(score {result['score']})"
        )

    reused = find_reused_passwords(credentials)
    lines.append("")
    if reused:
        lines.append("-- WARNING: Reused passwords detected --")
        for label, services in reused.items():
            lines.append(f"  {label}: used on {', '.join(services)}")
    else:
        lines.append("No password reuse detected. Good job!")

    return "\n".join(lines)


def export_report_to_csv(credentials: list[Credential], output_path: str) -> int:
    """Export a security summary (never plaintext passwords) to CSV.

    Args:
        credentials: The credentials to summarize.
        output_path: Destination path for the CSV file.

    Returns:
        The number of rows written.

    Raises:
        OSError: If the file cannot be written (propagated to caller
            so the CLI layer can decide how to report it).
    """
    fieldnames = ["id", "service", "username", "strength_rating", "strength_score"]

    with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for credential in credentials:
            result = analyze_strength(credential.password)
            writer.writerow(
                {
                    "id": credential.entry_id,
                    "service": credential.service,
                    "username": credential.username,
                    "strength_rating": result["rating"],
                    "strength_score": result["score"],
                }
            )

    return len(credentials)
