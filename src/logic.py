class LogAnalyzer:
    """Analyze security log entries and count log levels."""

    def __init__(self, log_lines):
        self.log_lines = log_lines

    def count_levels(self):
        """Count INFO, WARNING, and ERROR entries."""
        counts = {
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
        }

        for line in self.log_lines:
            parts = line.strip().split()

            if len(parts) < 3:
                continue

            level = parts[2].upper()

            if level in counts:
                counts[level] += 1

        return counts