"""Unit tests for the log-analysis logic."""

from src.logic import LogAnalyzer


def test_failed_login_is_parsed():
    """Verify that a failed SSH login is parsed correctly."""
    analyzer = LogAnalyzer(threshold=3)

    line = (
        "Sep 17 00:01:01 webserver sshd[1001]: "
        "Failed password for admin from 192.168.1.50 port 50101 ssh2"
    )

    event = analyzer.parse_line(line)

    assert event is not None
    assert event.status == "FAILED"
    assert event.username == "admin"
    assert event.source_ip == "192.168.1.50"


def test_successful_login_is_parsed():
    """Verify that a successful SSH login is parsed correctly."""
    analyzer = LogAnalyzer()

    line = (
        "Sep 17 00:02:01 webserver sshd[1002]: "
        "Accepted password for analyst from 172.16.0.10 port 51001 ssh2"
    )

    event = analyzer.parse_line(line)

    assert event is not None
    assert event.status == "SUCCESS"
    assert event.source_ip == "172.16.0.10"


def test_suspicious_ip_is_detected():
    """Verify repeated failed attempts trigger the threshold."""
    analyzer = LogAnalyzer(threshold=2)

    lines = [
        (
            "Sep 17 00:01:01 webserver sshd[1]: "
            "Failed password for admin from 10.0.0.5 port 1 ssh2"
        ),
        (
            "Sep 17 00:01:02 webserver sshd[2]: "
            "Failed password for admin from 10.0.0.5 port 2 ssh2"
        ),
        (
            "Sep 17 00:01:03 webserver sshd[3]: "
            "Accepted password for admin from 10.0.0.10 port 3 ssh2"
        ),
    ]

    result = analyzer.analyze(lines)

    assert result.failed_logins == 2
    assert result.successful_logins == 1
    assert result.suspicious_ips == {"10.0.0.5": 2}
