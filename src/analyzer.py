import re
from collections import Counter

IP_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

KEYWORDS = {
    "failed_login": ["failed login", "login failed", "authentication failed"],
    "warning": ["warning"],
    "error": ["error"],
    "critical": ["critical"],
    "denied": ["denied", "access denied"],
}


def extract_ip_addresses(text: str) -> list[str]:
    """Extract IPv4 addresses from text."""

    return re.findall(IP_PATTERN, text)


def count_security_events(text: str) -> dict[str, int]:
    """Count security events without double-counting overlapping phrases."""

    event_counts = {
        event_type: 0
        for event_type in KEYWORDS
    }

    for line in text.lower().splitlines():
        for event_type, phrases in KEYWORDS.items():
            if any(phrase in line for phrase in phrases):
                event_counts[event_type] += 1

    return event_counts


def analyze_text_file(file_path: str) -> dict:
    """Analyze a text-based evidence file for security indicators."""

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    ip_addresses = extract_ip_addresses(content)
    event_counts = count_security_events(content)

    return {
        "ip_addresses": ip_addresses,
        "ip_counts": dict(Counter(ip_addresses)),
        "events": event_counts,
    }