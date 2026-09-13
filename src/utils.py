import os


def validate_directory(directory_path: str) -> None:
    """Validate that the supplied evidence directory can be scanned."""

    if not os.path.exists(directory_path):
        raise FileNotFoundError(
            f"Evidence directory '{directory_path}' does not exist."
        )

    if not os.path.isdir(directory_path):
        raise NotADirectoryError(
            f"'{directory_path}' is not a directory."
        )

    if not os.listdir(directory_path):
        raise ValueError(
            f"Evidence directory '{directory_path}' is empty."
        )