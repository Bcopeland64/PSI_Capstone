from utils import read_log_file, validate_log_file
from analyzer import LogAnalyzer
import pandas as pd
import matplotlib.pyplot as plt


def main():
    """Run the cybersecurity log analyzer."""

    file_path = "data/sample.log"

    # Validate input file
    if not validate_log_file(file_path):
        print("Error: Invalid or missing log file.")
        return

    # Read log file
    lines = read_log_file(file_path)

    if not lines:
        print("Error: Log file is empty.")
        return

    # Analyze logs
    analyzer = LogAnalyzer(lines)
    analyzer.analyze()

    ip_counts, error_count = analyzer.get_results()

    # Display results
    print("=== Cybersecurity Log Analyzer ===")
    print(f"Total log lines: {len(lines)}")
    print(f"Total errors: {error_count}")

    print("\nIP Address Activity:")

    for ip, count in ip_counts.items():
        print(f"{ip}: {count} events")

    # Prepare data for CSV
    data = []

    for ip, count in ip_counts.items():
        data.append({
            "IP Address": ip,
            "Events": count
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save report
    df.to_csv("data/report.csv", index=False)

    print("\nReport saved to data/report.csv")

    # Create graph
    plt.figure(figsize=(8, 5))
    plt.bar(df["IP Address"], df["Events"])
    plt.xlabel("IP Address")
    plt.ylabel("Number of Events")
    plt.title("IP Address Activity")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save graph
    plt.savefig("data/ip_activity.png")
    plt.close()

    print("Graph saved to data/ip_activity.png")


if __name__ == "__main__":
    main()