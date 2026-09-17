SEVERITY_SCORES = {
    "Low": 1,
    "Medium": 3,
    "High": 6,
    "Critical": 10,
}

class Alert:
    """Represents a single security alert."""

    def __init__(self, alert_id, alert_type, severity, source_ip):
        self.alert_id = alert_id
        self.alert_type = alert_type
        self.severity = severity
        self.source_ip = source_ip
        self.score = SEVERITY_SCORES.get(severity, 0)

    def __repr__(self):
        return f"{self.alert_id} | {self.alert_type} | {self.severity} | Score: {self.score}"
