"""Core business logic for security incident triage."""

from collections import Counter

from src.models import Incident
from src.utils import (
    clean_text,
    parse_timestamp,
    validate_incident_id,
    validate_ip,
    validate_required_fields,
)


class TriageEngine:
    """Create, validate, score, and summarize security incidents."""

    ATTACK_SCORES = {
        "port scan": 1,
        "brute force": 2,
        "phishing": 3,
        "sql injection": 4,
        "malware": 5,
    }

    def create_incident(self, row: dict) -> Incident:
        """Validate raw data and return an Incident object."""
        validate_required_fields(row)

        incident_id = clean_text(row["incident_id"])
        source_ip = clean_text(row["source_ip"])
        destination_ip = clean_text(row["destination_ip"])
        attack_type = clean_text(row["attack_type"])
        username = clean_text(row["username"])
        description = clean_text(row["description"])
        timestamp = parse_timestamp(clean_text(row["timestamp"]))

        validate_incident_id(incident_id)

        if not validate_ip(source_ip):
            raise ValueError(f"Invalid source IP: {source_ip}")

        if not validate_ip(destination_ip):
            raise ValueError(
                f"Invalid destination IP: {destination_ip}"
            )

        incident = Incident(
            incident_id=incident_id,
            timestamp=timestamp,
            source_ip=source_ip,
            destination_ip=destination_ip,
            attack_type=attack_type,
            username=username,
            description=description,
        )

        score = self.calculate_score(attack_type)
        severity = self.score_to_severity(score)
        incident.set_triage_result(severity, score)

        return incident

    def calculate_score(self, attack_type: str) -> int:
        """Return the configured risk score for an attack type."""
        return self.ATTACK_SCORES.get(attack_type.lower(), 1)

    @staticmethod
    def score_to_severity(score: int) -> str:
        """Convert a numeric score into a severity level."""
        if score >= 5:
            return "CRITICAL"
        if score >= 4:
            return "HIGH"
        if score >= 3:
            return "MEDIUM"
        return "LOW"

    def analyze(self, incidents: list[Incident]) -> dict:
        """Return summary statistics for a collection of incidents."""
        severity_counts = Counter(
            incident.severity for incident in incidents
        )
        attack_counts = Counter(
            incident.attack_type for incident in incidents
        )

        return {
            "total": len(incidents),
            "critical": severity_counts.get("CRITICAL", 0),
            "high": severity_counts.get("HIGH", 0),
            "medium": severity_counts.get("MEDIUM", 0),
            "low": severity_counts.get("LOW", 0),
            "attack_types": dict(attack_counts),
        }
