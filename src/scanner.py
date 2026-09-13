import hashlib
import os

from src.models import EvidenceFile


def calculate_sha256(file_path: str) -> str:
    """Calculate and return the SHA-256 hash of a file."""

    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


def scan_directory(directory_path: str) -> list[EvidenceFile]:
    """Scan a directory and collect metadata about each file."""

    evidence_files = []

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            try:
                size_bytes = os.path.getsize(file_path)
                modified_time = os.path.getmtime(file_path)
                extension = os.path.splitext(filename)[1].lower()
                sha256 = calculate_sha256(file_path)

                evidence_file = EvidenceFile(
                    name=filename,
                    path=file_path,
                    extension=extension,
                    size_bytes=size_bytes,
                    modified_time=modified_time,
                    sha256=sha256,
                )

                evidence_files.append(evidence_file)

            except (PermissionError, OSError) as error:
                print(f"Warning: Could not process '{file_path}': {error}")

    return evidence_files