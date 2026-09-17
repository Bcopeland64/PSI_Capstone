"""Command-line interface for SecTriage.

Subcommands:
    full        Run every collector against a target folder and print/save a report.
    processes   Print a snapshot of running processes.
    files       Hash, timeline, and duplicate-check a folder.
    logs        Summarize a text log file (levels, IPs, failed logins).
    network     Summarize a traffic/connections CSV.
    history     List or inspect previously saved triage runs (SQLite).

Run `python main.py <subcommand> --help` for the options of any one command.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .collectors import FileSystemCollector, LogAnalyzer, NetworkAnalyzer, ProcessCollector
from .data_handler import ReportDatabase, export_summary_csv, save_report_json
from .exceptions import TriageError
from .models import TriageReport
from .utils import now_iso

try:
    from rich.console import Console
    from rich.table import Table

    _console: Optional["Console"] = Console()
except ImportError:  # rich is optional -- fall back to plain print()
    _console = None


def _print_header(title: str) -> None:
    if _console:
        _console.rule(f"[bold cyan]{title}")
    else:
        print(f"\n--- {title} ---")


def _print_table(headers: List[str], rows: List[list]) -> None:
    """Print tabular data with rich if available, else as plain aligned text."""
    if not rows:
        print("  (none)")
        return
    if _console:
        table = Table(show_header=True, header_style="bold magenta")
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        _console.print(table)
    else:
        widths = [max(len(str(h)), *(len(str(row[i])) for row in rows)) for i, h in enumerate(headers)]
        print("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
        for row in rows:
            print("  ".join(str(cell).ljust(w) for cell, w in zip(row, widths)))


# --------------------------------------------------------------------------
# Subcommand implementations
# --------------------------------------------------------------------------

def cmd_processes(args: argparse.Namespace) -> None:
    processes = ProcessCollector().collect(limit=args.limit)
    _print_header("Running Processes (sample)")
    _print_table(["PID", "Name"], [[p.pid, p.name] for p in processes])


def cmd_files(args: argparse.Namespace) -> None:
    collector = FileSystemCollector()

    _print_header(f"File Hashes — {args.folder}")
    records = collector.scan(args.folder)
    _print_table(
        ["File", "Size (bytes)", "SHA-256 (short)"],
        [[r.name, r.size_bytes, r.sha256[:16] + "..."] for r in records],
    )

    _print_header(f"Recently Modified (last {args.window}s)")
    recent = collector.recent(args.folder, window_seconds=args.window)
    _print_table(["File", "Age"], [[name, f"{age}s ago"] for name, age in recent])

    _print_header("Duplicate Content Groups")
    duplicates = collector.find_duplicates(args.folder)
    _print_table(
        ["SHA-256 (short)", "Files"],
        [[digest[:16] + "...", ", ".join(names)] for digest, names in duplicates.items()],
    )


def cmd_logs(args: argparse.Namespace) -> None:
    summary = LogAnalyzer().analyze(args.path, failed_login_marker=args.marker)
    _print_header(f"Log Summary — {args.path}")
    print(f"  Total lines: {summary.total_lines}")
    _print_table(["Level", "Count"], [[level, count] for level, count in summary.level_counts.items()])
    print(f"\n  Unique IPs seen: {len(summary.unique_ips)}")
    _print_header("Top Offenders (by failed logins)")
    _print_table(["IP", "Failed Attempts"], [[ip, count] for ip, count in summary.top_offenders])

    if args.filter_out:
        count = LogAnalyzer().write_filtered(args.path, args.filter_out, args.marker)
        print(f"\n  Wrote {count} matching line(s) to '{args.filter_out}'.")


def cmd_network(args: argparse.Namespace) -> None:
    suspicious = set(args.suspicious_ports.split(",")) if args.suspicious_ports else None
    summary = NetworkAnalyzer().analyze_csv(args.path, suspicious_ports=suspicious)
    _print_header(f"Network Summary — {args.path}")
    print(f"  Total rows: {summary.total_rows}")
    _print_header("Top Destination Ports")
    _print_table(["Port", "Connections"], [[port, count] for port, count in summary.top_ports])
    _print_header("Top Talkers (by bytes)")
    _print_table(["Source IP", "Total Bytes"], [[ip, total] for ip, total in summary.top_talkers_by_bytes])
    _print_header("Suspicious Port Hits")
    _print_table(
        ["Timestamp", "Src IP", "Dst Port"],
        [[row.get("timestamp"), row.get("src_ip"), row.get("dst_port")] for row in summary.suspicious_hits],
    )


def cmd_full(args: argparse.Namespace) -> None:
    collector = FileSystemCollector()
    report = TriageReport(
        target=args.folder,
        generated_at=now_iso(),
        processes=ProcessCollector().collect(limit=args.process_limit),
        recent_files=collector.recent(args.folder, window_seconds=args.window),
        file_hashes=collector.scan(args.folder),
        duplicate_groups=collector.find_duplicates(args.folder),
    )

    if args.log:
        report.log_summary = LogAnalyzer().analyze(args.log)
    if args.csv:
        report.network_summary = NetworkAnalyzer().analyze_csv(args.csv)

    _print_header(f"Triage Report — {report.target}")
    print(f"  Generated: {report.generated_at}")

    _print_header("Running Processes (sample)")
    _print_table(["PID", "Name"], [[p.pid, p.name] for p in report.processes])

    _print_header(f"Recently Modified Files (last {args.window}s)")
    _print_table(["File", "Age"], [[name, f"{age}s ago"] for name, age in report.recent_files])

    _print_header("File Hashes")
    _print_table(
        ["File", "Size (bytes)", "SHA-256 (short)"],
        [[r.name, r.size_bytes, r.sha256[:16] + "..."] for r in report.file_hashes],
    )

    if report.duplicate_groups:
        _print_header("⚠ Duplicate Content Detected")
        _print_table(
            ["SHA-256 (short)", "Files"],
            [[digest[:16] + "...", ", ".join(names)] for digest, names in report.duplicate_groups.items()],
        )

    if report.log_summary:
        _print_header(f"Log Summary — {report.log_summary.source}")
        print(f"  Total lines: {report.log_summary.total_lines}, level counts: {report.log_summary.level_counts}")
        _print_table(["IP", "Failed Attempts"], [[ip, c] for ip, c in report.log_summary.top_offenders])

    if report.network_summary:
        _print_header(f"Network Summary — {report.network_summary.source}")
        _print_table(["Port", "Connections"], [[p, c] for p, c in report.network_summary.top_ports])

    if args.save_json:
        save_report_json(report, args.save_json)
        print(f"\nSaved full report to '{args.save_json}'.")

    if args.save_csv:
        export_summary_csv(report, args.save_csv)
        print(f"Saved CSV summary to '{args.save_csv}'.")

    if args.save_db:
        with ReportDatabase(args.db_path) as db:
            run_id = db.save_run(report)
            print(f"Saved run #{run_id} to history database '{args.db_path}'.")


def cmd_history(args: argparse.Namespace) -> None:
    with ReportDatabase(args.db_path) as db:
        if args.show is not None:
            run = db.get_run(args.show)
            if run is None:
                print(f"No run #{args.show} found in '{args.db_path}'.")
                return
            _print_header(f"Run #{args.show}")
            print(f"  Target:    {run['target']}")
            print(f"  Generated: {run['generated_at']}")
            print(f"  Files:     {len(run['file_hashes'])}")
            print(f"  Duplicate groups: {len(run['duplicate_groups'])}")
        else:
            rows = db.list_runs(limit=args.limit)
            _print_header(f"Triage Run History ({args.db_path})")
            _print_table(
                ["ID", "Target", "Generated", "Files", "Dup Groups"],
                [[r["id"], r["target"], r["generated_at"], r["file_count"], r["duplicate_group_count"]] for r in rows],
            )


# --------------------------------------------------------------------------
# Argument parser
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sectriage",
        description="End-to-end security triage toolkit (log, network, filesystem, process analysis).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_full = subparsers.add_parser("full", help="Run every collector against a target folder.")
    p_full.add_argument("folder", nargs="?", default="sample_data/sample_evidence", help="Target evidence folder.")
    p_full.add_argument("--window", type=int, default=600, help="Recent-file window in seconds (default: 600).")
    p_full.add_argument("--process-limit", type=int, default=5, help="Max processes to sample (default: 5).")
    p_full.add_argument("--log", help="Optional log file to include in the report.")
    p_full.add_argument("--csv", help="Optional traffic CSV to include in the report.")
    p_full.add_argument("--save-json", help="Path to save the full report as JSON.")
    p_full.add_argument("--save-csv", help="Path to save a flat CSV summary.")
    p_full.add_argument("--save-db", action="store_true", help="Save this run to the SQLite history database.")
    p_full.add_argument("--db-path", default="sectriage_history.db", help="SQLite database path.")
    p_full.set_defaults(func=cmd_full)

    p_proc = subparsers.add_parser("processes", help="Print a snapshot of running processes.")
    p_proc.add_argument("--limit", type=int, default=10)
    p_proc.set_defaults(func=cmd_processes)

    p_files = subparsers.add_parser("files", help="Hash, timeline, and duplicate-check a folder.")
    p_files.add_argument("folder")
    p_files.add_argument("--window", type=int, default=600)
    p_files.set_defaults(func=cmd_files)

    p_logs = subparsers.add_parser("logs", help="Summarize a text log file.")
    p_logs.add_argument("path")
    p_logs.add_argument("--marker", default="Failed password", help="Substring marking a failed-login line.")
    p_logs.add_argument("--filter-out", help="If set, write matching lines to this path.")
    p_logs.set_defaults(func=cmd_logs)

    p_net = subparsers.add_parser("network", help="Summarize a traffic/connections CSV.")
    p_net.add_argument("path")
    p_net.add_argument("--suspicious-ports", help="Comma-separated ports to flag, e.g. 4444,31337.")
    p_net.set_defaults(func=cmd_network)

    p_hist = subparsers.add_parser("history", help="List or inspect previously saved triage runs.")
    p_hist.add_argument("--db-path", default="sectriage_history.db")
    p_hist.add_argument("--limit", type=int, default=10)
    p_hist.add_argument("--show", type=int, help="Show full detail for one run ID.")
    p_hist.set_defaults(func=cmd_history)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point used by main.py. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        args.func(args)
    except TriageError as exc:
        # Analyst-friendly message instead of a raw traceback for expected,
        # recoverable problems (missing file, bad folder, malformed CSV...).
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())
