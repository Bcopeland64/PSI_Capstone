import argparse
import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.analyzer import analyze_text_file
from src.models import TriageResult
from src.reporter import save_csv_report, save_json_summary
from src.risk import calculate_risk_score
from src.scanner import scan_directory
from src.utils import validate_directory

console = Console()

def main():
    """Run the Digital Evidence Triage Tool."""

    parser = argparse.ArgumentParser(
        description="Scan digital evidence and generate a security triage report."
    )

    parser.add_argument(
        "directory",
        help="Path to the directory containing evidence files.",
    )

    parser.add_argument(
        "--output",
        default="reports",
        help="Directory where reports will be saved. Default: reports",
    )

    args = parser.parse_args()

    try:
        validate_directory(args.directory)
        evidence_files = scan_directory(args.directory)

    except (FileNotFoundError, NotADirectoryError, ValueError) as error:
        print(f"Error: {error}")
        return

    total_score = 0
    all_reasons = []
    overall_risk = "LOW"
    triage_results = []

    for evidence_file in evidence_files:
        if evidence_file.extension in [".txt", ".log"]:
            analysis = analyze_text_file(evidence_file.path)

            score, risk_level, reasons = calculate_risk_score(analysis)

            triage_result = TriageResult(
            evidence_file=evidence_file,
            ip_addresses=analysis["ip_addresses"],
            event_counts=analysis["events"],
            risk_score=score,
            risk_level=risk_level,
            reasons=reasons,
            )

            triage_results.append(triage_result)

            total_score += score
            all_reasons.extend(reasons)

            if risk_level == "CRITICAL":
                overall_risk = "CRITICAL"
            elif risk_level == "HIGH" and overall_risk != "CRITICAL":
                overall_risk = "HIGH"
            elif (
                risk_level == "MEDIUM"
                and overall_risk not in ["HIGH", "CRITICAL"]
            ):
                overall_risk = "MEDIUM"

    csv_path = os.path.join(args.output, "evidence_report.csv")
    json_path = os.path.join(args.output, "triage_summary.json")

    save_csv_report(triage_results, csv_path)

    summary = {
        "files_scanned": len(evidence_files),
        "total_risk_score": total_score,
        "overall_risk_level": overall_risk,
        "reasons": all_reasons,
    }

    save_json_summary(summary, json_path)

    table = Table(title="Digital Evidence Triage Summary")

    table.add_column("Metric", style="cyan")
    table.add_column("Result", style="bold")

    table.add_row("Files Scanned", str(len(evidence_files)))
    table.add_row("Overall Risk", overall_risk)
    table.add_row("Total Risk Score", str(total_score))
    table.add_row("Report Directory", args.output)

    console.print()
    console.print(table)

    console.print(
        Panel(
            "Triage completed successfully.",
            title="Status",
        )
    )


if __name__ == "__main__":
    main()
