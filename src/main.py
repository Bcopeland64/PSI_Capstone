import os
import sys
import time
import matplotlib.pyplot as plt

from .data_handler import analyze_artifacts, read_artifacts, write_report
from .logic import (
    check_processes,
    find_duplicates,
    get_file_evidence,
    check_port,
    run_command,
    check_url,
)
from .utils import print_header, validate_folder


def run_triage(folder, artifacts_path=None):
    """Run all triage checks and generate a combined report."""

    print_header("DFIR END-TO-END TRIAGE")
    print(f"Target folder: {folder}")

    # 1. Running processes
    print_header("Running Processes")
    processes = check_processes()
    if processes:
        for process in processes:
            print(f"PID: {process.pid:<8} Name: {process.name}")
    else:
        print("No process information available.")

    # 2. File evidence
    print_header("File Evidence")
    evidence = get_file_evidence(folder)
    if evidence:
        for item in evidence:
            modified = time.ctime(item.modified_time)
            status = "RECENT" if item.recent else "normal"
            print(f"File: {item.name}")
            print(f"  Size: {item.size} bytes")
            print(f"  Modified: {modified}")
            print(f"  SHA-256: {item.sha256}")
            print(f"  Status: {status}\n")
    else:
        print("No files found.")

    # 3. Duplicate files
    print_header("Duplicate Files")
    duplicates = find_duplicates(folder)
    if duplicates:
        for file_hash, names in duplicates.items():
            print(f"Hash: {file_hash}")
            print(f"Files: {', '.join(names)}")
    else:
        print("No duplicate files found.")

    # 4. CSV artifacts
    artifact_stats = {}
    if artifacts_path:
        print_header("Forensic Artifact Analysis")
        rows = read_artifacts(artifacts_path)
        artifact_stats = analyze_artifacts(rows)
        print(f"Total events: {artifact_stats['total_events']}")
        print("\nEvents by type:")
        for event_type, count in artifact_stats["by_type"].items():
            print(f"  {event_type}: {count}")
        print("\nEvents by hour:")
        for hour, count in artifact_stats["by_hour"].items():
            print(f"  {hour}:00 -> {count}")

                # Visualization with matplotlib (Stacked Bar Chart)
        if rows:
            events_by_hour_type = {}
            for row in rows:
                ts = row.get("timestamp", "")
                etype = row.get("event_type", "unknown")
                if len(ts) >= 13:
                    hour = ts[11:13]
                    if hour not in events_by_hour_type:
                        events_by_hour_type[hour] = {
                            "process_started": 0,
                            "file_created": 0,
                            "file_deleted": 0
                        }
                    if etype in events_by_hour_type[hour]:
                        events_by_hour_type[hour][etype] += 1

            hours = sorted(events_by_hour_type.keys())
            process_started = [events_by_hour_type[h]["process_started"] for h in hours]
            file_created = [events_by_hour_type[h]["file_created"] for h in hours]
            file_deleted = [events_by_hour_type[h]["file_deleted"] for h in hours]

            import numpy as np
            plt.figure(figsize=(8,6))
            x = np.arange(len(hours))
            plt.bar(x, process_started, label="process_started", color="blue")
            plt.bar(x, file_created, bottom=process_started, label="file_created", color="orange")
            plt.bar(x, file_deleted, bottom=np.array(process_started)+np.array(file_created), label="file_deleted", color="green")

            plt.xticks(x, hours)
            plt.xlabel("Hour of Day")
            plt.ylabel("Number of Events")
            plt.title("Events by Type per Hour")
            plt.legend()
            os.makedirs("reports", exist_ok=True)
            plt.savefig("reports/artifact_stacked.png")
            print("Stacked chart saved to reports/artifact_stacked.png")



    # 5. Network Ports
    print_header("Network Ports")
    if check_port("127.0.0.1", 80):
        print("Port 80 open")
    else:
        print("Port 80 closed")

    # 6. System Command
    print_header("System Command")
    whoami_output = run_command(["whoami"])
    print("whoami ->", whoami_output)

    # 7. HTTP Requests
    print_header("HTTP Requests")
    urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/403",
        "https://httpbin.org/status/404"
    ]
    http_results = {}
    for u in urls:
        status = check_url(u)
        http_results[u] = status
        print(f"{u} -> {status}")

    # Build report
    report = {
        "target_folder": folder,
        "generated_at": time.ctime(),
        "process_count": len(processes),
        "file_count": len(evidence),
        "recent_files": [item.name for item in evidence if item.recent],
        "duplicate_files": duplicates,
        "artifact_analysis": artifact_stats,
        "port_80_open": check_port("127.0.0.1", 80),
        "whoami": whoami_output,
        "http_checks": http_results,
    }
    return report


def main():
    """Main entry point for the application."""
    folder = sys.argv[1] if len(sys.argv) > 1 else "data/sample_evidence"
    artifacts_path = sys.argv[2] if len(sys.argv) > 2 else "data/artifacts.csv"

    if not validate_folder(folder):
        return

    report = run_triage(folder, artifacts_path)

    os.makedirs("reports", exist_ok=True)
    output_path = "reports/triage_report.json"

    if write_report(report, output_path):
        print_header("Report Complete")
        print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
