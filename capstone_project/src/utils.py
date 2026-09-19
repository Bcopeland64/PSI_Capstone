import os
import ipaddress


def file_exists(file_path):
    """Check if a file exists."""
    return os.path.isfile(file_path)


def validate_ip(ip_address):
    """Check if an IP address is valid."""
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def validate_port(port):
    """Check if a port number is valid."""
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False
    