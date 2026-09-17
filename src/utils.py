import ipaddress
from pathlib import Path

def validate_ip(ip_address: str) -> bool:
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def check_file_exists(file_path: str) -> Path:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"file not exist: {file_path}")
    return path