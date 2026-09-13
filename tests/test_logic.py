from src.logic import LogAnalyzer


def test_count_levels():
    """Test INFO, WARNING, and ERROR counting."""
    log_lines = [
        "2026-09-11 09:15:22 INFO Login successful",
        "2026-09-11 09:20:11 ERROR Failed login",
        "2026-09-11 09:22:45 WARNING Failed login",
    ]

    analyzer = LogAnalyzer(log_lines)
    counts = analyzer.count_levels()

    assert counts["INFO"] == 1
    assert counts["WARNING"] == 1
    assert counts["ERROR"] == 1