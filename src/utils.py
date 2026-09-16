"""Helper functions: input validation for the Password Vault CLI.

Every function here is a pure function (no hidden state, no I/O side
effects beyond what is explicitly documented) so it can be unit
tested in isolation.
"""


class ValidationError(Exception):
    """Raised when user-supplied data fails validation."""


def validate_master_password(raw_password: str) -> str:
    """Validate the master password used to unlock/initialize the vault.

    Args:
        raw_password: The raw string typed by the user.

    Returns:
        The validated master password.

    Raises:
        ValidationError: If the password is too short or empty.
    """
    if not raw_password:
        raise ValidationError("Master password cannot be empty.")
    if len(raw_password) < 8:
        raise ValidationError("Master password must be at least 8 characters.")
    return raw_password


def validate_service(raw_service: str) -> str:
    """Validate a service/site name.

    Args:
        raw_service: The raw string typed by the user.

    Returns:
        The trimmed service name.

    Raises:
        ValidationError: If the service name is empty or too long.
    """
    service = raw_service.strip()
    if not service:
        raise ValidationError("Service name cannot be empty.")
    if len(service) > 100:
        raise ValidationError("Service name must be under 100 characters.")
    return service


def validate_username(raw_username: str) -> str:
    """Validate a username/email string.

    Args:
        raw_username: The raw string typed by the user.

    Returns:
        The trimmed username.

    Raises:
        ValidationError: If the username is empty.
    """
    username = raw_username.strip()
    if not username:
        raise ValidationError("Username cannot be empty.")
    return username


def validate_password(raw_password: str) -> str:
    """Validate a credential password before storing it.

    This only enforces a non-empty value -- strength feedback is
    handled separately by `security.analyze_strength`, since a weak
    password is still a valid (if inadvisable) one to store.

    Args:
        raw_password: The raw password typed by the user.

    Returns:
        The validated password.

    Raises:
        ValidationError: If the password is empty.
    """
    if not raw_password:
        raise ValidationError("Password cannot be empty.")
    return raw_password


def validate_positive_int(raw_value: str, field_name: str = "value") -> int:
    """Validate a string as a positive integer.

    Args:
        raw_value: The raw string typed by the user.
        field_name: Name used in error messages.

    Returns:
        The parsed positive integer.

    Raises:
        ValidationError: If the value is not a positive integer.
    """
    try:
        value = int(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"'{raw_value}' is not a valid {field_name}.") from exc

    if value <= 0:
        raise ValidationError(f"{field_name} must be a positive integer.")
    return value
