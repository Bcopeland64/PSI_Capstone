import os


def read_log_file(file_path):
    """Read a log file and return its lines."""
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError

        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return []

    except PermissionError:
        print(f"Error: Permission denied: {file_path}")
        return []

    except OSError as error:
        print(f"Error reading file: {error}")
        return []


def validate_log_file(file_path):
    """Validate that the log file exists and has the correct extension."""
    if not file_path:
        return False

    if not file_path.lower().endswith(".log"):
        return False

    return os.path.isfile(file_path)