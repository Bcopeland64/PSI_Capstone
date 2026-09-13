class ValidationError(Exception):
    """Used when a user's input is not valid."""
    pass


def require_non_empty(value, field_name):
    """Return text when it is not blank."""
    stripped = value.strip()
    if not stripped:
        raise ValidationError(field_name + " cannot be empty")
    return stripped


def require_int_in_range(value, field_name, low, high):
    """Return an integer when it is inside the allowed range."""
    try:
        parsed = int(value)
    except ValueError:
        raise ValidationError(field_name + " must be a whole number")
    if parsed < low or parsed > high:
        raise ValidationError(field_name + " must be between " + str(low) + " and " + str(high))
    return parsed


def prompt_until_valid(prompt_text, validator, max_attempts=5):
    """Keep asking until the input passes validation."""
    attempt = 0
    while attempt < max_attempts:
        raw = input(prompt_text)
        try:
            return validator(raw)
        except ValidationError as error:
            print("Invalid input:", error)
        attempt += 1
    print("Too many invalid attempts. Cancelled.")
    return None
