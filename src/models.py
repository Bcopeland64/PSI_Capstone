"""
models.py
---------
Defines how a single alert and a source-IP summary are represented,
as plain dictionaries, plus the functions that build and classify them.
"""



def make_alert(timestamp: str, source_ip: str, username: str,
               event_type: str, failed_attempts: int) -> dict:
    """
    Build a dictionary representing one security alert.
    timestamp is kept as plain text (e.g. "2026-09-01 12:00:00") —
    that way this dict can be saved to JSON with no extra steps later.
    """
    return {
        "timestamp": timestamp,
        "source_ip": source_ip,
        "username": username,
        "event_type": event_type,
        "failed_attempts": failed_attempts,
        "severity": "LOW",  # default until classify_alert() runs
    }


def classify_alert(alert: dict) -> str:
    """
    Decide how serious this alert is and store it in alert["severity"].

    Rules:
    - "privilege escalation" is always CRITICAL (no legitimate everyday reason
      for this to happen, so no threshold needed).
    - "root login attempt" starts at HIGH, but becomes CRITICAL if there are
      2 or more failed attempts (one attempt could be a real admin; repeated
      attempts look like guessing).
    - Otherwise, severity is based purely on failed_attempts:
        10+  -> CRITICAL
        5-9  -> HIGH
        1-4  -> MEDIUM
        0    -> LOW
    """
    event = alert["event_type"].strip().lower()
    attempts = alert["failed_attempts"]

    if event == "privilege escalation":
        severity = "CRITICAL"
    elif event == "root login attempt":
        severity = "CRITICAL" if attempts >= 2 else "HIGH"
    elif attempts >= 10:
        severity = "CRITICAL"
    elif attempts >= 5:
        severity = "HIGH"
    elif attempts >= 1:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    alert["severity"] = severity
    return severity

def make_source_summary(source_ip: str, total_failed_attempts: int,
                         event_types: list, highest_severity: str,
                         alert_count: int) -> dict:
    """Build a dictionary summarizing all alerts seen from one source IP."""
    return {
        "source_ip": source_ip,
        "total_failed_attempts": total_failed_attempts,
        "event_types": sorted(set(event_types)),
        "highest_severity": highest_severity,
        "alert_count": alert_count,
    }

