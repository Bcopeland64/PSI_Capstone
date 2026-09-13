from pathlib import Path
import hashlib

def write_report(lines, report_path):
    
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )
    
def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()