# SentryTriage — Security Triage & Incident-Response CLI

**Track chosen:** Interactive CLI / Utility Tool (with elements of the Data
Analytics track for the log-analysis command).

## Purpose

SentryTriage is a command-line toolkit for a first-pass security triage. It
brings together the techniques from the Python-for-Security intensive
(HTTP requests, CSV log parsing, file hashing, timelines, port scanning,
process listing) into one small, modular application that a SOC analyst
could realistically reach for:

- **`logs`** — parse a network-connection CSV export, tally protocols, flag
  connections to watch-listed ports, find the top talker by total bytes, and
  optionally look up geolocation/ISP for offending source IPs.
- **`files`** — hash every file in an evidence folder, build a chronological
  timeline, flag anything modified within a recent time window, and detect
  duplicate content hiding under different filenames (a classic
  rename-to-evade trick).
- **`ports`** — scan a range of TCP ports on a host you're authorized to test
  (e.g. `127.0.0.1`), printing open/closed for each.
- **`processes`** — list running processes, using `psutil` if available and
  falling back to `ps aux` otherwise.
- **`report`** — run any combination of the above in one pass, write a full
  JSON report and a flat CSV summary, and save a row to a local SQLite
  history table.
- **`history`** — show the most recent past triage runs from that SQLite
  database.

## Requirements

Python 3.10+. Third-party packages:

```bash
pip install -r requirements.txt
```

`psutil` is optional — the `processes` command and `report --include-processes`
fall back to `ps aux` (via `subprocess`) if it isn't installed. `requests` is
used for the optional IP-reputation lookup in `logs --check-reputation`; if
there's no network access, that lookup fails gracefully and reports
`lookup_failed` instead of crashing the run.

## How to run

All commands are run from the project root as a module, so `src` resolves
as a package:

```bash
# Analyze the sample connection log
python -m src.main logs data/sample_data.csv

# Same, but also look up geolocation for any watchlisted source IPs
python -m src.main logs data/sample_data.csv --check-reputation

# Scan the sample evidence folder
python -m src.main files data/sample_evidence

# Port-scan localhost, ports 1-1024 (only ever scan hosts you're authorized to test)
python -m src.main ports 127.0.0.1 1 1024

# List running processes
python -m src.main processes --limit 10

# Run a full triage and persist it
python -m src.main report --csv-path data/sample_data.csv --folder data/sample_evidence --host 127.0.0.1 --start-port 1 --end-port 100

# Review past runs
python -m src.main history
```

## Example output

```
$ python -m src.main logs data/sample_data.csv

Parsed 10 connection(s) from data/sample_data.csv
Protocol counts: {'tcp': 8, 'udp': 2}
Top talker: 192.168.1.9 (44.2 KB)

Watchlist hits (4):
  2026-02-10T10:00:15  192.168.1.7 -> port 8080 (tcp)
  2026-02-10T10:00:30  192.168.1.9 -> port 4444 (tcp)
  2026-02-10T10:00:36  192.168.1.9 -> port 4444 (tcp)
  2026-02-10T10:00:47  192.168.1.9 -> port 4444 (tcp)
```

## Design notes

- **Modular architecture:** `models.py` (data classes), `utils.py`
  (validation + hashing helpers, no I/O), `data_handler.py` (all disk/DB
  I/O — CSV, JSON, SQLite), `logic.py` (pure analysis functions, no I/O),
  and `main.py` (argparse CLI wiring it all together). Keeping I/O out of
  `logic.py` is what makes the functions in `tests/test_logic.py` easy to
  test without touching disk.
- **Data persistence:** connection logs and the watchlist are read from
  CSV/JSON; every `report` run is written to `triage_report.json` /
  `triage_report.csv` and additionally inserted into a SQLite database
  (`data/triage_history.db`) so past runs can be reviewed with `history`.
- **Error handling & validation:** malformed CSV rows are skipped (with a
  count reported) instead of crashing the run; host/port inputs are
  validated before scanning; the reputation lookup and process listing both
  degrade gracefully instead of raising; `main()` has a top-level catch-all
  so the CLI never dumps a raw traceback at the user.
- **External integration:** `requests` for the optional IP-reputation
  lookup; `psutil` as an optional dependency for process listing.

## Known limitations

- The port scanner is intentionally simple (sequential, no async) — fine
  for a handful of ports on a local/authorized host, not a substitute for a
  real scanner like `nmap` on large ranges.
- `check-reputation` depends on a free public API (`ip-api.com`) and will
  report `lookup_failed` with no internet access or if rate-limited.
- The SQLite history stores the full report JSON per row for simplicity
  rather than a normalized schema — fine at CLI scale, not meant to be a
  production audit log.

## Ethics note

Only scan hosts and networks you own or are explicitly authorized to test.
The sample data and defaults here point at `127.0.0.1` and bundled sample
files for exactly this reason.
