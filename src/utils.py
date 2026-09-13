import requests
def validate_file_path(file_path):
    """Validate that the user entered a non-empty file path."""
    if not file_path or not file_path.strip():
        raise ValueError("File path cannot be empty.")

    return file_path.strip()
def validate_log_level(level):
    """Validate a log level entered by the user."""
    valid_levels = {"INFO", "WARNING", "ERROR"}

    level = level.strip().upper()

    if level not in valid_levels:
        raise ValueError(
            "Invalid log level. Choose INFO, WARNING, or ERROR."
        )

    return level


def check_connection():
    """Check internet connection using an external HTTP request."""
    try:
        response = requests.get("https://example.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
