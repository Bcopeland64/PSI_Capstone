import os


def validate_folder(folder):
    """Check that the supplied path is a valid folder."""
    if not os.path.exists(folder):
        print(f"Error: '{folder}' does not exist.")
        return False

    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a folder.")
        return False

    return True


def print_header(title):
    """Print a simple section header."""
    print()
    print("=" * 50)
    print(title)
    print("=" * 50)