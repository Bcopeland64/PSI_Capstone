"""
utils.py
Input validation utilities and helper functions.
"""

import re


def validate_severity(severity: str) -> bool:
    """Validates if severity input is within allowed values."""
    valid_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    return severity.strip().upper() in valid_levels


def validate_ip(ip_str: str) -> bool:
    """Validates an IPv4 address structure using regex."""
    pattern = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.){3}(25[0-5]|(2[0-4]|1\d|[1-9]|)\d)$"
    return bool(re.match(pattern, ip_str.strip()))


def get_valid_input(prompt: str, validation_func, error_message: str) -> str:
    """Generic loop helper for capturing valid user input."""
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        print(f"[Invalid Input] {error_message}")