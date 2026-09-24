"""Business logic for cybersecurity triage."""


def calculate_risk(case):
    """Calculate a risk score from case indicators and update the case."""
    score = 0

    if case.executable:
        score += 2
    if case.downloaded:
        score += 2
    if case.antivirus_triggered:
        score += 4
    if case.suspicious_extension:
        score += 2

    case.risk_score = min(score, 10)

    if case.risk_score >= 7:
        case.risk_level = "HIGH"
    elif case.risk_score >= 4:
        case.risk_level = "MEDIUM"
    else:
        case.risk_level = "LOW"

    return case


def get_recommendation(risk_level):
    """Return a simple recommended action for the risk level."""
    recommendations = {
        "HIGH": "Isolate the file/system and investigate the incident.",
        "MEDIUM": "Perform additional analysis and monitor the system.",
        "LOW": "Continue normal monitoring and keep security controls active.",
    }
    return recommendations.get(risk_level, "Review the case manually.")


def search_cases(cases, keyword):
    """Search cases by case ID, file name, or notes."""
    keyword = keyword.lower()
    return [
        case for case in cases
        if keyword in case.case_id.lower()
        or keyword in case.file_name.lower()
        or keyword in case.notes.lower()
    ]
