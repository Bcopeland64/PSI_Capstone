from src.logic import get_running_processes, analyze_process, get_recent_files
from src.utils import write_report, calculate_sha256


def main():
    processes = get_running_processes()
    recent_files = get_recent_files("data")

    report_lines = []

    report_lines.append(f"Found {len(processes)} running processes.\n")

    report_lines.append("Recent files:")

    for file in recent_files:
        file_hash = calculate_sha256(file["path"])

        report_lines.append(f"Path: {file['path']}")
        report_lines.append(f"Modified: {file['modified_time']}")
        report_lines.append(f"SHA-256: {file_hash}")
        report_lines.append("")

    report_lines.append("Process triage:")

    for process in processes:
        risk, reasons = analyze_process(process)

        if risk == "REVIEW":
            report_lines.append(f"Process: {process.get('name')}")
            report_lines.append(f"PID: {process.get('pid')}")
            report_lines.append(f"Risk: {risk}")
            report_lines.append(f"Reasons: {', '.join(reasons)}")
            report_lines.append("")

    write_report(
        report_lines,
        "reports/process_report.txt"
    )

    print("Report created: reports/process_report.txt")


if __name__ == "__main__":
    main()