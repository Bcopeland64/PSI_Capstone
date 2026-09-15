"""
utils.py
--------
Stateless helper functions: input validation, parsing, and display
formatting. Nothing here touches the database or the priority-scoring
rules, which keeps these functions trivial to unit test.
"""

from src.models import Category, Priority, Status


class ValidationError(Exception):
    """Raised when user-supplied input fails validation."""


def require_non_empty(value: str, field_name: str) -> str:
    """
    Ensure a string field is present and not just whitespace.

    Raises ValidationError with a message naming the offending field,
    so the CLI layer can show it directly to the user.
    """
    if value is None or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return value.strip()


def parse_choice(raw: str, valid_values: list[str], field_name: str) -> str:
    """
    Validate that `raw` (case-insensitive) matches one of valid_values.
    Returns the canonical (upper-case) value on success.
    """
    if raw is None:
        raise ValidationError(f"{field_name} is required.")
    candidate = raw.strip().upper()
    if candidate not in valid_values:
        options = ", ".join(valid_values)
        raise ValidationError(f"Invalid {field_name} '{raw}'. Choose one of: {options}")
    return candidate


def parse_category(raw: str) -> Category:
    return Category(parse_choice(raw, Category.values(), "category"))


def parse_priority(raw: str) -> Priority:
    return Priority(parse_choice(raw, Priority.values(), "priority"))


def parse_status(raw: str) -> Status:
    return Status(parse_choice(raw, Status.values(), "status"))


def parse_positive_int(raw: str, field_name: str) -> int:
    """Parse a string into a positive integer, raising ValidationError otherwise."""
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a whole number.")
    if value <= 0:
        raise ValidationError(f"{field_name} must be greater than zero.")
    return value


def truncate(text: str, width: int = 40) -> str:
    """Shorten text for tidy table display, adding an ellipsis if cut."""
    text = text or ""
    return text if len(text) <= width else text[: width - 1] + "…"


def priority_badge(priority: Priority) -> str:
    """Return a small text badge used for CLI table output."""
    badges = {
        Priority.LOW: "[LOW]",
        Priority.MEDIUM: "[MED]",
        Priority.HIGH: "[HIGH]",
        Priority.CRITICAL: "[CRIT]",
    }
    return badges.get(priority, f"[{priority.value}]")
