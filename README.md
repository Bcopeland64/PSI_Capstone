<<<<<<< HEAD
# SecTriage — End-to-End Security Triage Toolkit

**Capstone project — Python for Security, 3-Day Intensive**

## Purpose

Combines the three days of the workshop into one working analyst tool:

| Day | Skill                                    | Where it lives                              |
|-----|-------------------------------------------|----------------------------------------------|
| 1   | Log parsing, regex, `.split()`, Counter   | `sectriage/collectors.py` → `LogAnalyzer`     |
| 2   | HTTP requests, CSV parsing, OS/process info | `sectriage/collectors.py` → `NetworkAnalyzer`, `ProcessCollector` |
| 3   | File hashing, timelines, structured export | `sectriage/collectors.py` → `FileSystemCollector` |

Given a target evidence folder (plus optional log/CSV files), it collects a
process snapshot, a file-modification timeline, SHA-256 hashes, duplicate
(renamed) files, log-level/failed-login breakdowns, and network summaries —
then prints a combined report and can save it as JSON, CSV, or into a
running SQLite history.

## Requirements

Python 3.9+. No third-party package is *required* — the tool degrades
gracefully without them:

| Package  | Used for                          | If missing                              |
|----------|------------------------------------|------------------------------------------|
| `psutil` | cross-platform process listing     | falls back to `ps aux` / `tasklist`       |
| `rich`   | pretty tables                      | falls back to plain aligned text          |
| `requests` | live HTTP endpoint checks        | reports "requests not installed" per URL  |

To install everything (recommended for the full experience):

```bash
pip install -r requirements.txt
```

## Project Structure

```
sectriage_project/
├── main.py                  # entry point: python main.py <command> ...
├── requirements.txt
├── sectriage/
│   ├── __init__.py
│   ├── cli.py                # argparse subcommands, output formatting
│   ├── collectors.py          # ProcessCollector, FileSystemCollector, LogAnalyzer, NetworkAnalyzer
│   ├── data_handler.py        # JSON/CSV export, SQLite run history (ReportDatabase)
│   ├── models.py              # dataclasses: ProcessRecord, FileRecord, LogSummary, NetworkSummary, TriageReport
│   ├── exceptions.py          # TriageError, InvalidTargetError, UnsupportedFormatError, PersistenceError
│   └── utils.py                # hash_file, iter_files, human_age, now_iso
├── tests/
│   ├── test_utils.py
│   └── test_collectors.py
└── sample_data/                # ready-to-run demo data
    ├── sample_auth.log
    ├── sample_traffic.csv
    └── sample_evidence/         # includes one duplicated/renamed file on purpose
```

## How to Run

**Full combined report** (uses the bundled sample data by default):

```bash
python main.py full sample_data/sample_evidence \
    --log sample_data/sample_auth.log \
    --csv sample_data/sample_traffic.csv \
    --save-json report.json \
    --save-csv summary.csv \
    --save-db
```

**Individual checks:**

```bash
python main.py processes                          # running process snapshot
python main.py files sample_data/sample_evidence   # hashes, recent files, duplicates
python main.py logs sample_data/sample_auth.log    # level counts, IPs, failed-login offenders
python main.py network sample_data/sample_traffic.csv --suspicious-ports 4444,31337
python main.py history                             # list past --save-db runs
python main.py history --show 1                    # full detail for one past run
```

Every subcommand has its own `--help`, e.g. `python main.py logs --help`.

## Example Output

```
--- Triage Report — sample_data/sample_evidence ---
  Generated: 2026-09-17T10:05:53

--- Running Processes (sample) ---
PID  Name
1    process_api
...

--- ⚠ Duplicate Content Detected ---
SHA-256 (short)      Files
919b3e64fcad31d3...  dropper.bin, svchost_backup.bin

--- Log Summary — sample_data/sample_auth.log ---
  Total lines: 10, level counts: {'WARNING': 1}
IP             Failed Attempts
45.33.12.9     4
185.220.101.5  2
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

(Written with the standard-library `unittest`, so they run with zero extra
installs; `pytest tests/` also discovers and runs them if you have pytest.)

## Design Notes

- **Modular architecture:** collectors, models, persistence, and the CLI are
  separate modules so each can be tested and reused independently.
- **OOP:** each data-gathering concern is its own class
  (`ProcessCollector`, `FileSystemCollector`, `LogAnalyzer`,
  `NetworkAnalyzer`); records are typed `dataclasses` rather than loose
  dicts.
- **Data persistence:** JSON (full report), CSV (flat summary), and SQLite
  (`ReportDatabase`, for run-over-run history) are all supported.
- **Error handling:** a small custom exception hierarchy
  (`sectriage/exceptions.py`) is caught once at the CLI boundary, so bad
  input (missing files, malformed CSV columns, unreadable folders) prints a
  one-line message and a non-zero exit code instead of a raw traceback.
- **External packages:** `requests` for live HTTP checks, `psutil` for
  process listing, `rich` for table rendering — each with a working
  fallback if not installed.

## Known Limitations

- `network`'s live port-scan helper (`NetworkAnalyzer.check_port`) only
  targets `localhost` by default, per the workshop's authorized-use rule;
  pass `allow_remote=True` in code only for hosts you're explicitly
  authorized to test.
- Process listing without `psutil` parses `ps aux` / `tasklist` output
  positionally, which is "good enough for triage" but not as robust as a
  real process API.
- The `sectriage_history.db` SQLite file is created in the current working
  directory unless `--db-path` is given.
=======
# cybersecurity-py
>>>>>>> ea93d34913a1bd24a453c43b81f89a59718a4912
