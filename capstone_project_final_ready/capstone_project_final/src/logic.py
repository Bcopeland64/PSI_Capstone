"""Core SSH authentication log parsing and triage logic."""

import re
from collections import Counter

from .models import LogEvent, TriageResult
from .utils import is_valid_ip


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<host>\S+)\s+sshd\[\d+\]:\s+(?P<message>.*)$"
)

FAILED_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\S+) "
    r"from (?P<ip>\S+)"
)

SUCCESS_PATTERN = re.compile(
    r"Accepted \S+ for (?P<user>\S+) from (?P<ip>\S+)"
)


class LogAnalyzer:
    """Analyze SSH authentication logs for triage indicators."""

    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.events: list[LogEvent] = []

    def parse_line(self, line: str) -> LogEvent | None:
        """Parse one SSH authentication log line."""
        match = LOG_PATTERN.match(line)
        if not match:
            return None

        timestamp = match.group("timestamp")
        host = match.group("host")
        message = match.group("message")

        failed = FAILED_PATTERN.search(message)
        if failed and is_valid_ip(failed.group("ip")):
            return LogEvent(
                timestamp=timestamp,
                host=host,
                username=failed.group("user"),
                source_ip=failed.group("ip"),
                status="FAILED",
                raw_message=line,
            )

        success = SUCCESS_PATTERN.search(message)
        if success and is_valid_ip(success.group("ip")):
            return LogEvent(
                timestamp=timestamp,
                host=host,
                username=success.group("user"),
                source_ip=success.group("ip"),
                status="SUCCESS",
                raw_message=line,
            )

        return LogEvent(
            timestamp=timestamp,
            host=host,
            username=None,
            source_ip=None,
            status="OTHER",
            raw_message=line,
        )

    def analyze(self, lines: list[str]) -> TriageResult:
        """Parse lines and calculate triage indicators."""
        self.events = []

        for line in lines:
            event = self.parse_line(line)
            if event is not None:
                self.events.append(event)

        failed = [e for e in self.events if e.status == "FAILED"]
        successful = [e for e in self.events if e.status == "SUCCESS"]
        other = [e for e in self.events if e.status == "OTHER"]

        failed_ips = Counter(
            event.source_ip for event in failed if event.source_ip
        )

        suspicious_ips = {
            ip: count
            for ip, count in failed_ips.items()
            if count >= self.threshold
        }

        suspicious_events = sum(
            1 for event in failed if event.source_ip in suspicious_ips
        )

        unique_ips = {
            event.source_ip
            for event in self.events
            if event.source_ip
        }

        return TriageResult(
            total_events=len(self.events),
            failed_logins=len(failed),
            successful_logins=len(successful),
            other_events=len(other),
            unique_ips=len(unique_ips),
            suspicious_ips=dict(
                sorted(
                    suspicious_ips.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            ),
            suspicious_event_count=suspicious_events,
        )
