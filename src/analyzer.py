class LogAnalyzer:
    """Analyze cybersecurity log data."""

    def __init__(self, lines):
        self.lines = lines
        self.ip_counts = {}
        self.error_count = 0

    def analyze(self):
        """Analyze log lines."""
        for line in self.lines:
            parts = line.split()

            if len(parts) < 2:
                continue

            if "ERROR" in line:
                self.error_count += 1

            ip_address = parts[-1]

            if ip_address.count(".") == 3:
                self.ip_counts[ip_address] = (
                    self.ip_counts.get(ip_address, 0) + 1
                )

    def get_results(self):
        """Return analysis results."""
        return self.ip_counts, self.error_count