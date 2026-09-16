import json

from logic import check_ip_reputation, sort_by_severity
from utils import load_alerts

DATA_FILE = "data/alerts.csv"
REPORT_FILE = "data/triage_report.json"

def save_report(alerts, filename=REPORT_FILE):
    """Save the sorted results to a JSON report file."""
    report = [
        {"id": a.alert_id, "type": a.alert_type, "severity": a.severity, "score": a.score}
        for a in alerts
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to: {filename}")

def main():
    alerts = load_alerts(DATA_FILE)
    if not alerts:
        print("No valid alerts to sort.")
        return

    sorted_alerts = sort_by_severity(alerts)

    print("=== Triage Results (highest severity first) ===")
    for alert in sorted_alerts:
        print(alert)

    top_alert = sorted_alerts[0]
    location = check_ip_reputation(top_alert.source_ip)
    print(f"\nTop-priority alert ({top_alert.alert_id}) source IP location: {location}")

    save_report(sorted_alerts)

if __name__ == "__main__":
    main()
