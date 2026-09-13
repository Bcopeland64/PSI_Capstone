def calculate_risk_score(analysis: dict) -> tuple[int, str, list[str]]:
    """Calculate a risk score, level, and reasons from analysis results."""

    score = 0
    reasons = []

    events = analysis.get("events", {})
    ip_counts = analysis.get("ip_counts", {})

    failed_logins = events.get("failed_login", 0)
    warnings = events.get("warning", 0)
    errors = events.get("error", 0)
    critical = events.get("critical", 0)
    denied = events.get("denied", 0)

    if failed_logins > 0:
        score += failed_logins * 2
        reasons.append(f"{failed_logins} failed login event(s) detected")

    if warnings > 0:
        score += warnings
        reasons.append(f"{warnings} warning event(s) detected")

    if errors > 0:
        score += errors * 2
        reasons.append(f"{errors} error event(s) detected")

    if critical > 0:
        score += critical * 4
        reasons.append(f"{critical} critical event(s) detected")

    if denied > 0:
        score += denied
        reasons.append(f"{denied} denied access event(s) detected")

    repeated_ips = {
        ip: count
        for ip, count in ip_counts.items()
        if count >= 3
    }

    if repeated_ips:
        score += 2
        reasons.append("Repeated activity from the same IP address detected")

    if score >= 10:
        risk_level = "CRITICAL"
    elif score >= 6:
        risk_level = "HIGH"
    elif score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return score, risk_level, reasons