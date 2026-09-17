import csv

from models import Alert

def load_alerts(filename):
    """Read alerts from a CSV file and return a list of Alert objects.

    Wrapped in try/except so a missing file prints a clear message
    instead of crashing the program.
    """
    alerts = []
    try:
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("alert_id") or not row.get("severity"):
                    print(f"Warning: skipping incomplete row: {row}")
                    continue
                alert = Alert(
                    alert_id=row["alert_id"],
                    alert_type=row["alert_type"],
                    severity=row["severity"],
                    source_ip=row["source_ip"],
                )
                alerts.append(alert)
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
    return alerts
