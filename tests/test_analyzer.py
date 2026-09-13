from src.analyzer import count_security_events, extract_ip_addresses


def test_extract_ip_addresses():
    """Test that IPv4 addresses are extracted correctly."""

    text = (
        "Connection from 45.33.12.9 followed by "
        "another connection from 10.0.0.5."
    )

    result = extract_ip_addresses(text)

    assert result == ["45.33.12.9", "10.0.0.5"]


def test_count_security_events():
    """Test that security event keywords are counted correctly."""

    text = """
    FAILED LOGIN from 45.33.12.9
    WARNING suspicious connection
    ERROR connection failure
    CRITICAL system failure
    ACCESS DENIED
    """

    result = count_security_events(text)

    assert result["failed_login"] == 1
    assert result["warning"] == 1
    assert result["error"] == 1
    assert result["critical"] == 1
    assert result["denied"] == 1