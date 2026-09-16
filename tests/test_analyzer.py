from src.analyzer import LogAnalyzer


def test_error_count():
    lines = [
        "2026-09-16 10:00:00 ERROR Failed login from 10.0.0.5",
        "2026-09-16 10:01:00 INFO User login from 192.168.1.10",
    ]

    analyzer = LogAnalyzer(lines)
    analyzer.analyze()

    _, error_count = analyzer.get_results()

    assert error_count == 1


def test_ip_count():
    lines = [
        "2026-09-16 10:00:00 ERROR Failed login from 10.0.0.5",
        "2026-09-16 10:01:00 ERROR Failed login from 10.0.0.5",
        "2026-09-16 10:02:00 INFO User login from 192.168.1.10",
    ]

    analyzer = LogAnalyzer(lines)
    analyzer.analyze()

    ip_counts, _ = analyzer.get_results()

    assert ip_counts["10.0.0.5"] == 2
    assert ip_counts["192.168.1.10"] == 1