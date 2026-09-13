from datetime import datetime, timedelta


VALID_STATUSES = ("open", "in_progress", "resolved", "closed")


class Ticket:
   
    def __init__(self, title, description, reporter, ticket_id=None,
                 severity="unclassified", team="unassigned", status="open",
                 created_at=None, due_at=None):
        self.ticket_id = ticket_id
        self.title = title
        self.description = description
        self.reporter = reporter
        self.severity = severity
        self.team = team
        self.status = status
        if created_at is None:
            self.created_at = datetime.now().isoformat(timespec="seconds")
        else:
            self.created_at = created_at
        self.due_at = due_at


    def mark_status(self, new_status):
        if new_status not in VALID_STATUSES:
            raise ValueError("Invalid status: " + new_status)
        self.status = new_status


    def compute_due_date(self, sla_hours):
        created = datetime.fromisoformat(self.created_at)
        self.due_at = (created + timedelta(hours=sla_hours)).isoformat(timespec="seconds")

    def is_overdue(self, now=None):
        if self.due_at is None or self.status in ("resolved", "closed"):
            return False
        if now is None:
            now = datetime.now()
        return now > datetime.fromisoformat(self.due_at)


    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "title": self.title,
            "description": self.description,
            "reporter": self.reporter,
            "severity": self.severity,
            "team": self.team,
            "status": self.status,
            "created_at": self.created_at,
            "due_at": self.due_at,
        }

def ticket_from_dict(row):
  
    return Ticket(
        title=row["title"],
        description=row["description"],
        reporter=row["reporter"],
        ticket_id=row.get("ticket_id"),
        severity=row.get("severity", "unclassified"),
        team=row.get("team", "unassigned"),
        status=row.get("status", "open"),
        created_at=row.get("created_at"),
        due_at=row.get("due_at"),
    )
