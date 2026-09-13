def calculate_priority(severity):
    """Calculate the priority based on incident severity."""
    if severity == "Critical":
        return "Critical"
    elif severity == "High":
        return "High"
    elif severity == "Medium":
        return "Medium"
    else:
        return "Low"


def count_by_severity(incidents):
    """Count incidents according to their severity."""
    counts = {
        "Low": 0,
        "Medium": 0,
        "High": 0,
        "Critical": 0,
    }

    for incident in incidents:
        severity = incident.get("severity")

        if severity in counts:
            counts[severity] += 1

    return counts