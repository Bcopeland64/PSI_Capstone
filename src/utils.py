def validate_severity(severity):
    """Check whether the severity level is valid."""
    valid_severities = ["Low", "Medium", "High", "Critical"]
    return severity in valid_severities


def get_non_empty_input(message):
    """Get input and make sure it is not empty."""
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Input cannot be empty. Please try again.")