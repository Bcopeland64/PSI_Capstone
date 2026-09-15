# Support Ticket Triage System 🛠️

A capstone project for the Python Workshop — an **Interactive CLI Utility Tool**
that logs incoming support tickets, automatically scores and prioritizes them
with a rule-based triage engine, and persists everything to a SQLite database.

## Why this project

Real support/helpdesk teams need to quickly figure out *what's on fire* among
a pile of incoming reports. This tool automates the first triage pass: every
ticket is scanned for urgency signals (category + keywords) and assigned a
`priority_score` (0–100) and a `Priority` level (`LOW` → `CRITICAL`), so the
most dangerous issues always float to the top of the list.

## Features

- **Log tickets** with title, description, category, and reporter — priority
  is assigned automatically, not typed in by hand.
- **List tickets** sorted by urgency (priority rank, then score).
- **View full details** of any ticket by ID.
- **Update ticket status** through its lifecycle: `OPEN → IN_PROGRESS →
  RESOLVED → CLOSED`.
- **Summary report**: totals, breakdown by status/priority/category, average
  urgency score.
- **CSV import/export** for interoperability with spreadsheets — a sample
  dataset is included at `data/sample_data.csv`.
- **Delete tickets** with a confirmation prompt.
- Robust **input validation** and **error handling** throughout — malformed
  input, missing files, and bad database state never crash the app.

## Project structure

```
capstone_project/
├── data/
│   └── sample_data.csv     # sample tickets you can import right away
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point / menu loop
│   ├── models.py            # Ticket, Priority, Status, Category (OOP core)
│   ├── logic.py              # TriageEngine (scoring rules) + reporting
│   ├── data_handler.py       # SQLite persistence + CSV import/export
│   └── utils.py               # validation & formatting helpers
├── tests/
│   └── test_logic.py          # pytest unit tests (14 tests)
├── .gitignore
├── requirements.txt
└── README.md
```

### Why this layout

- **`models.py`** — pure data: the `Ticket` dataclass and the `Priority`,
  `Status`, `Category` enums. No logic lives here, just the shape of a ticket.
- **`logic.py`** — the `TriageEngine` class encapsulates the scoring rules
  (keyword weights + category baselines + thresholds) as pure functions with
  no side effects, so they're trivial to unit test in isolation from the
  database.
- **`data_handler.py`** — the only module that talks to SQLite. The
  `TicketRepository` class exposes `add`, `get`, `list_all`, `update`,
  `delete`, `export_csv`, `import_csv`, and translates every `sqlite3.Error`
  into a single `DataHandlerError` so callers only handle one exception type.
- **`utils.py`** — stateless validation/formatting helpers with zero
  dependency on the database or scoring rules.
- **`main.py`** — the CLI shell. Wires the above together, handles all user
  I/O, and catches every `ValidationError`/`DataHandlerError` so bad input
  never crashes the program.

## How the triage engine works

Each ticket's title + description is scanned (case-insensitively) for urgent
keywords (`"outage"`, `"breach"`, `"data loss"`, `"crash"`, etc.), and its
category contributes a baseline score (e.g. `SECURITY` and `OUTAGE` start
higher than `FEATURE_REQUEST`). The scores are summed, clamped to 0–100, and
mapped onto a priority level via configurable thresholds:

| Score range | Priority   |
|-------------|-----------|
| 60–100      | CRITICAL  |
| 35–59       | HIGH      |
| 15–34       | MEDIUM    |
| 0–14        | LOW       |

This is intentionally simple and fully transparent — see `src/logic.py` to
adjust keyword weights or thresholds.

## Setup

Requires **Python 3.10+** (uses the `X | None` union type syntax and modern
`enum`/`dataclasses` features). No third-party packages are required to run
the app itself — only `pytest` is needed to run the test suite.

```bash
# from the capstone_project/ directory
pip install -r requirements.txt   # only needed to run tests
```

## Running the app

```bash
python -m src.main
```

You'll see a menu:

```
==================== SUPPORT TICKET TRIAGE ====================
 1. Log a new ticket (auto-triaged)
 2. List all tickets (sorted by urgency)
 3. View ticket details
 4. Update ticket status
 5. Show summary report
 6. Import tickets from CSV
 7. Export tickets to CSV
 8. Delete a ticket
 9. Exit
=================================================================
```

Try option **6** first and import `data/sample_data.csv` to see eight
pre-triaged tickets appear instantly, or use option **1** to log a new one
by hand.

Data persists in `data/tickets.db` (SQLite) between runs — it's created
automatically on first launch.

## Running the tests

```bash
pytest tests/ -v
```

14 tests cover the triage scoring rules (keyword weighting, score clamping,
priority thresholds), the reporting functions (`summarize`,
`sort_by_urgency`), and the input-validation helpers. All logic under test is
pure — no database or filesystem access is needed to run the suite.

## Possible extensions

- Add a `--web` mode with Flask/FastAPI reusing the same `logic.py`/`data_handler.py`.
- Swap the keyword-based `TriageEngine` for a call to an LLM API for smarter classification.
- Add ticket assignment to specific team members and SLA-deadline tracking.
