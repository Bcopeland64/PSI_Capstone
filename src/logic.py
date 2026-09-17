import re
import pandas as pd
from pathlib import Path
from src.models import SecurityAlert
from src.utils import check_file_exists, validate_ip

class NetLogSecAnalyzer:
    """Advanced security log analyzer with time-window detection and rule processing."""
    
    def __init__(self, log_file_path: str):
        self.file_path = check_file_exists(log_file_path)
        self.df = None

    def parse_logs(self):
        """Read log file, parse timestamps and IPs using Regex, and load into a Pandas DataFrame."""
        # Standard format example: 2026-09-17 10:15:20 - FAILED LOGIN - IP: 192.168.1.50 - User: admin
        log_pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<status>FAILED|SUCCESS) LOGIN - IP: (?P<ip>[\d\.]+) - User: (?P<user>\w+)"
        
        parsed_data = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.search(log_pattern, line)
                    if match:
                        data = match.groupdict()
                        # Validate IP to ensure security integrity
                        if validate_ip(data["ip"]):
                            parsed_data.append(data)
            
            if parsed_data:
                self.df = pd.DataFrame(parsed_data)
                # Convert timestamp string to actual datetime objects for chronological analysis
                self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
            else:
                self.df = pd.DataFrame(columns=["timestamp", "status", "ip", "user"])
                
        except Exception as e:
            raise RuntimeError(f"Error occurred while parsing log file: {e}")

    def detect_brute_force(self, time_window_minutes: int = 5, threshold: int = 3) -> list[SecurityAlert]:
        """Detect potential brute-force attacks within a specific rolling time window."""
        if self.df is None or self.df.empty:
            return []
            
        failed_df = self.df[self.df["status"] == "FAILED"].copy()
        if failed_df.empty:
            return []

        alerts = []
        # Group records by IP address
        for ip, group in failed_df.groupby("ip"):
            group = group.sort_values("timestamp")
            
            max_attempts_in_window = 0
            first_seen = None
            last_seen = None
            
            # Check rolling windows for threshold violations
            for i in range(len(group)):
                start_time = group.iloc[i]["timestamp"]
                end_time = start_time + pd.Timedelta(minutes=time_window_minutes)
                window_subset = group[(group["timestamp"] >= start_time) & (group["timestamp"] <= end_time)]
                
                if len(window_subset) >= threshold:
                    max_attempts_in_window = len(window_subset)
                    first_seen = window_subset["timestamp"].min()
                    last_seen = window_subset["timestamp"].max()
                    break
            
            if max_attempts_in_window >= threshold:
                # Assign severity based on failed attempts count
                severity = "High" if max_attempts_in_window >= 5 else "Medium"
                
                alert = SecurityAlert(
                    ip_address=ip,
                    rule_name="Brute Force Detection",
                    count=max_attempts_in_window,
                    first_seen=str(first_seen),
                    last_seen=str(last_seen),
                    severity=severity
                )
                alerts.append(alert)
                
        return alerts

    def export_comprehensive_report(self, output_csv: str):
        """Export the parsed log data into a CSV report."""
        if self.df is not None:
            self.df.to_csv(output_csv, index=False)