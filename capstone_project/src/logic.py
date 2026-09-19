import pandas as pd

from utils import file_exists, validate_ip, validate_port


SENSITIVE_PORTS = [21, 22, 23, 445, 3389]


class SecurityTriage:
    """Analyze security logs and identify potentially suspicious activity."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """Load security logs from a CSV file."""
        if not file_exists(self.file_path):
            print("Error: File not found.")
            return False

        try:
            self.data = pd.read_csv(self.file_path)

            if self.data.empty:
                print("Error: The CSV file is empty.")
                return False

            print("Data loaded successfully.")
            return True

        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty.")
            return False

        except Exception as error:
            print("Error:", error)
            return False

    def clean_data(self):
        """Clean and validate the security log data."""
        if self.data is None:
            print("Please load the data first.")
            return

        self.data.drop_duplicates(inplace=True)
        self.data.dropna(inplace=True)

        self.data["protocol"] = self.data["protocol"].str.upper()
        self.data["status"] = self.data["status"].str.lower()

        self.data["dst_port"] = pd.to_numeric(
            self.data["dst_port"],
            errors="coerce"
        )

        self.data["bytes"] = pd.to_numeric(
            self.data["bytes"],
            errors="coerce"
        )

        self.data.dropna(inplace=True)

        self.data = self.data[
            self.data["src_ip"].apply(validate_ip)
        ]

        self.data = self.data[
            self.data["dst_ip"].apply(validate_ip)
        ]

        self.data = self.data[
            self.data["dst_port"].apply(validate_port)
        ]

        print("Data cleaned and validated successfully.")

    def find_failed_logins(self):
        """Return all failed login events."""
        if self.data is None:
            print("Please load the data first.")
            return None

        return self.data[
            self.data["status"] == "failed"
        ]

    def find_sensitive_ports(self):
        """Return events using sensitive destination ports."""
        if self.data is None:
            print("Please load the data first.")
            return None

        return self.data[
            self.data["dst_port"].isin(SENSITIVE_PORTS)
        ]

    def top_source_ips(self, limit=5):
        """Return the most active source IP addresses."""
        if self.data is None:
            print("Please load the data first.")
            return None

        return self.data[
            "src_ip"
        ].value_counts().head(limit)

    def get_summary(self):
        """Return a summary of the security log analysis."""
        if self.data is None:
            print("Please load the data first.")
            return None

        failed_logins = len(
            self.data[
                self.data["status"] == "failed"
            ]
        )

        sensitive_events = len(
            self.data[
                self.data["dst_port"].isin(SENSITIVE_PORTS)
            ]
        )

        summary = {
            "total_events": len(self.data),
            "failed_logins": failed_logins,
            "sensitive_port_events": sensitive_events,
            "unique_source_ips": self.data["src_ip"].nunique()
        }

        return summary

    def generate_report(self, output_file):
        """Save suspicious events to a CSV report."""
        if self.data is None:
            print("Please load the data first.")
            return False

        report = self.data[
            (self.data["status"] == "failed")
            | (self.data["dst_port"].isin(SENSITIVE_PORTS))
        ]

        report.to_csv(
            output_file,
            index=False
        )

        print("Report generated successfully.")
        return True
    