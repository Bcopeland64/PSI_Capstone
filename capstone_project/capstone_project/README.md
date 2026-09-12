# Security Triage Toolkit

A small end-to-end CLI tool that combines the core skills from the Python
Workshop into one working application: network log analysis, file
integrity verification, local port checks, and external API integration.

## What it does

Run the tool and choose from a menu:

1. **Traffic log report** — parses a connections CSV and reports the top
   `src_ip` addresses by total bytes transferred, the busiest destination
   ports, and any connections hitting a watchlist of suspicious ports
   (e.g. `4444`, `31337`).
2. **File integrity check** — computes a file's SHA-256 hash and compares
   it against the last hash recorded for that file in a local SQLite
   database, reporting `first_seen`, `match`, or `mismatch`.
3. **Port check** — checks whether a given `host:port` is open, using a
   plain TCP connect attempt, and logs the result to the database.
4. **API demo** — fetches a fresh UUID from `https://httpbin.org/uuid` to
   demonstrate external API integration with error handling.
5. **History** — shows the most recent port checks recorded so far.

## Authorized-use note

The port-check feature is for **local or explicitly authorized targets
only** (e.g. `127.0.0.1`, a lab VM you own or have permission to test).
Never point it at third-party systems without authorization.

## Project structure

```
capstone_project/
├── data/
│   └── sample_data.csv     # sample traffic log for the demo report
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point / menu loop
│   ├── models.py            # Connection, FileHashRecord, TriageDatabase (SQLite)
│   ├── logic.py              # traffic analysis, hash verification, API calls
│   └── utils.py              # hashing, port checks, input validation helpers
├── tests/
│   └── test_logic.py        # pytest unit tests for logic.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
cd capstone_project
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the tool

Run as a module from the project root, so the relative imports inside
`src/` resolve correctly:

```bash
python -m src.main
```

On first run it creates `data/triage.db` (a SQLite file) to store hash
and port-check history between sessions. This file is git-ignored.

## Running the tests

```bash
pytest
```

## Design notes

- **Modular architecture**: `utils.py` holds low-level, dependency-free
  primitives (hashing, port checks, validation). `models.py` holds data
  classes and the SQLite persistence layer. `logic.py` composes those
  into the actual triage operations. `main.py` is a thin CLI shell that
  only handles menu display and input prompts — no business logic lives
  there, which makes `logic.py` easy to unit test without a terminal.
- **Error handling**: every external interaction (file I/O, network
  sockets, HTTP requests, user input) is wrapped so bad input or a
  missing file/host prints a clear message instead of crashing.
- **Data persistence**: hash history and port-check history survive
  between runs via SQLite (`data/triage.db`), so "did this file change
  since last time?" is a real, answerable question.
