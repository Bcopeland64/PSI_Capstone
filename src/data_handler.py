from pathlib import Path


def read_log_file(file_path):
    """Read log entries from an external text file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            return file.readlines()
    except OSError as error:
        raise OSError(f"Could not read file: {file_path}") from error


def save_results(results, output_file):
    """Save analysis results to a text file."""
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            for level, count in results.items():
                file.write(f"{level}: {count}\n")
    except OSError as error:
        raise OSError(
            f"Could not save results: {output_file}"
        ) from error