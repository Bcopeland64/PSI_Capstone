#!/usr/bin/env python3
"""
main.py
-------
SentryTriage CLI -- a small security triage & incident-response toolkit.

Subcommands:
    logs        Analyze a network-connection CSV log (protocols, watchlist, top talker).
    files       Scan a folder of evidence files (hashes, timeline, duplicates, recent activity).
    ports       Scan a range of TCP ports on a host (local/authorized targets only).
    processes   List running processes.
    report      Run a full triage across logs + files + ports and persist the result.
    history     Show recent past triage runs from the local SQLite database.

Run `python -m src.main <subcommand> --help` for per-command options.
"""

import argparse
import sys

from src import data_handler, logic
from src.utils import human_bytes, validate_existing_path


def cmd_logs(args: argparse.Namespace) -> int:
    try:
        csv_path = validate_existing_path(args.csv_path)
        connections, skipped = data_handler.load_connections(csv_path)
        watchlist = data_handler.load_watchlist(args.watchlist)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if skipped:
        print(f"warning: skipped {skipped} malformed row(s)")

    protocol_counts = logic.count_protocols(connections)
    hits = logic.find_watchlist_hits(connections, watchlist["watchlist_ports"])
    top_talker = logic.find_top_talker(connections)

    print(f"\nParsed {len(connections)} connection(s) from {csv_path}")
    print("Protocol counts:", dict(protocol_counts))

    if top_talker:
        print(f"Top talker: {top_talker['src_ip']} ({human_bytes(top_talker['total_bytes'])})")

    if hits:
        print(f"\nWatchlist hits ({len(hits)}):")
        for hit in hits:
            print(f"  {hit['timestamp']}  {hit['src_ip']} -> port {hit['dst_port']} ({hit['protocol']})")
        if args.check_reputation:
            print("\nReputation lookups for offending source IPs:")
            for ip in {hit["src_ip"] for hit in hits}:
                info = logic.check_ip_reputation(ip)
                print(f"  {ip}: country={info['country']} isp={info['isp']} status={info['status']}")
    else:
        print("\nNo watchlist hits.")
    return 0


def cmd_files(args: argparse.Namespace) -> int:
    try:
        folder = validate_existing_path(args.folder)
        watchlist = data_handler.load_watchlist(args.watchlist)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    artifacts = logic.scan_folder(folder)
    timeline = logic.build_timeline(artifacts)
    recent = logic.flag_recent_files(timeline, watchlist["recent_window_seconds"])
    duplicates = logic.find_duplicates(timeline)

    print(f"\nScanned {len(artifacts)} file(s) in {folder}")
    print("\nTimeline (oldest -> newest):")
    for a in timeline:
        print(f"  {a.modified_iso}  {a.name:<20} {human_bytes(a.size_bytes):>10}  {a.sha256[:12]}...")

    if recent:
        print(f"\nRecently modified (within {watchlist['recent_window_seconds']}s):")
        for r in recent:
            print(f"  {r['name']} ({r['age_seconds']}s ago)")

    if duplicates:
        print("\nDuplicate content groups (possible renamed/copied payloads):")
        for group in duplicates:
            print(f"  {group}")
    return 0


def cmd_ports(args: argparse.Namespace) -> int:
    try:
        results = logic.scan_port_range(args.host, args.start_port, args.end_port)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for r in results:
        status = "open" if r.is_open else "closed"
        print(f"{r.host}:{r.port} -> {status}")
    open_count = sum(1 for r in results if r.is_open)
    print(f"\n{open_count} open / {len(results)} scanned")
    return 0


def cmd_processes(args: argparse.Namespace) -> int:
    procs = logic.list_processes(limit=args.limit)
    print(f"Running processes (up to {args.limit}):")
    for p in procs:
        print(f"  {p}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    connections, artifacts, port_results = None, None, None
    watchlist = data_handler.load_watchlist(args.watchlist)

    if args.csv_path:
        try:
            connections, skipped = data_handler.load_connections(validate_existing_path(args.csv_path))
            if skipped:
                print(f"warning: skipped {skipped} malformed row(s)")
        except FileNotFoundError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    if args.folder:
        try:
            artifacts = logic.scan_folder(validate_existing_path(args.folder))
        except FileNotFoundError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    if args.host:
        try:
            port_results = logic.scan_port_range(args.host, args.start_port, args.end_port)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    process_count = len(logic.list_processes(limit=1000)) if args.include_processes else None

    report = logic.build_report(
        target=args.folder or args.csv_path or args.host or "unspecified",
        connections=connections,
        watchlist_ports=watchlist["watchlist_ports"],
        artifacts=artifacts,
        recent_window_seconds=watchlist["recent_window_seconds"],
        port_results=port_results,
        process_count=process_count,
    )

    data_handler.write_report_json(report, args.out_json)
    data_handler.write_report_csv_summary(report, args.out_csv)
    row_id = data_handler.save_report_to_history(report)

    print(f"Triage complete. Report saved to {args.out_json} and {args.out_csv}.")
    print(f"Recorded in scan history as run #{row_id}.")
    print(f"  watchlist hits: {len(report.watchlist_hits)}")
    print(f"  duplicate groups: {len(report.duplicate_groups)}")
    print(f"  recent files: {len(report.recent_files)}")
    print(f"  open ports: {report.open_ports}")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    rows = data_handler.fetch_history(limit=args.limit)
    if not rows:
        print("No triage runs recorded yet.")
        return 0
    print(f"Last {len(rows)} triage run(s):")
    for row in rows:
        print(
            f"  #{row['id']}  {row['generated_at']}  target={row['target']}  "
            f"hits={row['watchlist_hit_count']}  dup_groups={row['duplicate_group_count']}  "
            f"recent_files={row['recent_file_count']}  open_ports={row['open_port_count']}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentrytriage",
        description="A small security triage & incident-response CLI toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_logs = subparsers.add_parser("logs", help="Analyze a network-connection CSV log.")
    p_logs.add_argument("csv_path", help="Path to a connections CSV (timestamp,src_ip,dst_port,protocol,bytes).")
    p_logs.add_argument("--watchlist", default="data/watchlist.json", help="Path to watchlist JSON config.")
    p_logs.add_argument("--check-reputation", action="store_true", help="Look up geolocation for offending IPs.")
    p_logs.set_defaults(func=cmd_logs)

    p_files = subparsers.add_parser("files", help="Scan a folder of evidence files.")
    p_files.add_argument("folder", help="Folder to scan.")
    p_files.add_argument("--watchlist", default="data/watchlist.json", help="Path to watchlist JSON config.")
    p_files.set_defaults(func=cmd_files)

    p_ports = subparsers.add_parser("ports", help="Scan a TCP port range (authorized/local targets only).")
    p_ports.add_argument("host", help="Host to scan, e.g. 127.0.0.1.")
    p_ports.add_argument("start_port", type=int, help="First port in the range.")
    p_ports.add_argument("end_port", type=int, help="Last port in the range (inclusive).")
    p_ports.set_defaults(func=cmd_ports)

    p_procs = subparsers.add_parser("processes", help="List running processes.")
    p_procs.add_argument("--limit", type=int, default=20, help="Max processes to list.")
    p_procs.set_defaults(func=cmd_processes)

    p_report = subparsers.add_parser("report", help="Run a full triage and persist the report.")
    p_report.add_argument("--csv-path", help="Connections CSV to analyze.")
    p_report.add_argument("--folder", help="Evidence folder to scan.")
    p_report.add_argument("--host", help="Host to port-scan.")
    p_report.add_argument("--start-port", type=int, default=1, help="First port (with --host).")
    p_report.add_argument("--end-port", type=int, default=1024, help="Last port (with --host).")
    p_report.add_argument("--include-processes", action="store_true", help="Include a process count.")
    p_report.add_argument("--watchlist", default="data/watchlist.json", help="Path to watchlist JSON config.")
    p_report.add_argument("--out-json", default="triage_report.json", help="Where to write the JSON report.")
    p_report.add_argument("--out-csv", default="triage_report.csv", help="Where to write the CSV summary.")
    p_report.set_defaults(func=cmd_report)

    p_history = subparsers.add_parser("history", help="Show recent past triage runs.")
    p_history.add_argument("--limit", type=int, default=10, help="Number of past runs to show.")
    p_history.set_defaults(func=cmd_history)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # last-resort guard so the CLI never raw-tracebacks on the user
        print(f"unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
