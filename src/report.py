"""Report formatting and CSV export."""

import csv
import os
import time


def print_report(report):
    """Print the complete triage report to the terminal."""
    print("\n" + "=" * 60)
    print("END-TO-END TRIAGE REPORT")
    print("=" * 60)
    print(f"Target folder: {report['folder']}")

    print("\nRunning processes (sample):")
    for process in report["processes"]:
        print(f"  {process}")

    print("\nRecently modified files:")
    if report["recent_files"]:
        for item in report["recent_files"]:
            print(
                f"  {item['name']} - "
                f"{item['age_seconds']}s ago - {item['size']} bytes"
            )
    else:
        print("  none")

    print("\nFile hashes:")
    for item in report["file_hashes"]:
        print(f"  {item['name']}: {item['sha256']}")

    print("\nFile timeline:")
    for item in report["timeline"]:
        print(
            f"  {time.ctime(item['modified'])} | "
            f"{item['name']} | {item['sha256'][:12]}..."
        )

    print("=" * 60)


def export_csv(report, output_file):
    """Export file triage results to a CSV report."""
    parent = os.path.dirname(output_file)
    if parent:
        os.makedirs(parent, exist_ok=True)

    recent_names = {item["name"] for item in report["recent_files"]}

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["name", "path", "size", "modified", "sha256", "recent"]
        )

        for item in report["timeline"]:
            writer.writerow(
                [
                    item["name"],
                    item["path"],
                    item["size"],
                    time.ctime(item["modified"]),
                    item["sha256"],
                    "YES" if item["name"] in recent_names else "NO",
                ]
            )
