from .models import Ticket



SLA_HOURS = {
    "critical": 4,
    "high": 24,
    "medium": 72,
    "low": 168,  # one week
}


SEVERITY_KEYWORDS = {
    "critical": ["outage", "down", "data loss", "breach", "security incident", "cannot log in", "crash"],
    "high": ["error", "failing", "broken", "urgent", "blocked", "timeout"],
    "medium": ["slow", "bug", "incorrect", "unexpected", "glitch"],
    "low": ["question", "how do i", "feature request", "typo", "cosmetic"],
}


class TriageEngine:
    """Classify tickets using simple keyword rules."""

    def classify_severity(self, text):
        """Return a severity based on the first matching rule."""
        text = text.lower()
        for keyword in SEVERITY_KEYWORDS["critical"]:
            if keyword in text:
                return "critical"
        for keyword in SEVERITY_KEYWORDS["high"]:
            if keyword in text:
                return "high"
        for keyword in SEVERITY_KEYWORDS["medium"]:
            if keyword in text:
                return "medium"
        for keyword in SEVERITY_KEYWORDS["low"]:
            if keyword in text:
                return "low"
        return "low"

    def classify_team(self, text):
        """Return a team based on simple if statements."""
        text = text.lower()
        if "server" in text or "outage" in text or "database" in text or "slow" in text:
            return "infrastructure"
        if "invoice" in text or "payment" in text or "charge" in text or "subscription" in text:
            return "billing"
        if "password" in text or "unauthorized" in text or "phishing" in text or "security" in text:
            return "security"
        if "feature" in text or "button" in text or "page" in text or "typo" in text:
            return "product"
        return "support"

    def triage(self, ticket):
        """Set the severity, team, and deadline on a ticket."""
        combined_text = ticket.title + " " + ticket.description
        ticket.severity = self.classify_severity(combined_text)
        ticket.team = self.classify_team(combined_text)
        ticket.compute_due_date(SLA_HOURS[ticket.severity])
        return ticket

    @staticmethod
    def summarize(tickets):
        """Count tickets by severity, team, and status."""
        summary = {
            "total": len(tickets),
            "by_severity": {},
            "by_team": {},
            "by_status": {},
            "overdue": 0,
        }
        for ticket in tickets:
            if ticket.severity not in summary["by_severity"]:
                summary["by_severity"][ticket.severity] = 0
            summary["by_severity"][ticket.severity] += 1

            if ticket.team not in summary["by_team"]:
                summary["by_team"][ticket.team] = 0
            summary["by_team"][ticket.team] += 1

            if ticket.status not in summary["by_status"]:
                summary["by_status"][ticket.status] = 0
            summary["by_status"][ticket.status] += 1

            if ticket.is_overdue():
                summary["overdue"] += 1
        return summary
