class SecurityAlert:
    """Represents a detected security alert with timing and severity details."""
    
    def __init__(self, ip_address: str, rule_name: str, count: int, first_seen: str, last_seen: str, severity: str):
        self.ip_address = ip_address
        self.rule_name = rule_name
        self.count = count
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.severity = severity

    def to_dict(self) -> dict:
        """Convert the alert object to a dictionary for easy exporting (JSON/CSV)."""
        return {
            "ip_address": self.ip_address,
            "rule_name": self.rule_name,
            "attempts": self.count,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "severity": self.severity
        }

    def __repr__(self) -> str:
        return f"[{self.severity}] IP: {self.ip_address} | Rule: {self.rule_name} | Count: {self.count} | {self.first_seen} -> {self.last_seen}"