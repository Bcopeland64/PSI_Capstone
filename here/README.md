# Ticket Triage System

An end-to-end CLI tool that ingests support tickets, automatically classifies
their **severity** and **owning team**, assigns an **SLA deadline**, and
persists everything to a local SQLite database — with CSV import/export and
summary reporting on top.

Built as a Python Workshop capstone project: an **Interactive CLI / Utility
Tool** (Track 2), using a simple class, persistent storage, input validation,
CSV files, and SQLite.

## Why this project

Triage is a real bottleneck in any support or issue-tracking workflow: every
new ticket needs a severity rating, a team assignment, and a response-time
deadline before anyone can act on it. This tool automates that first pass
using transparent, rule-based keywords, so a human only has to review
edge cases instead of triaging every ticket from scratch.

## Features

- **Automatic triage** — severity (`critical`/`high`/`medium`/`low`) and team
  (`infrastructure`/`billing`/`security`/`product`/`support`) are inferred
  from the ticket's title and description using simple keyword rules.
- **SLA deadlines** — each severity level maps to a response window (4h for
  critical, up to 1 week for low), and the tool flags overdue tickets.
- **Persistent storage** — tickets are stored in a local SQLite database
  (`data/tickets.db`), so nothing is lost between runs.
- **CSV import/export** — bulk-load tickets from a CSV file, or export the
  current ticket store for use elsewhere (e.g. a spreadsheet).
- **Summary metrics** — counts by severity, team, status, and overdue count.
- **Input validation** — all interactive prompts are validated with clear
  retry messaging instead of crashing on bad input.

## Project structure

```
capstone_project/
├── data/
│   └── sample_data.csv     # Example tickets to try the "Import from CSV" option
├── src/
│   ├── __init__.py
│   ├── main.py             # CLI entry point — menu loop, wires everything together
│   ├── models.py           # Ticket class (state + lifecycle behavior)
│   ├── logic.py            # Simple severity/team rules, SLA, and summaries
│   ├── data_handler.py      # SQLite repository + CSV import/export
│   └── utils.py             # Input validation helpers
├── tests/
│   └── test_logic.py        # pytest unit tests
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
cd capstone_project
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

```bash
python -m src.main
```

You'll see a plain text menu:

```text
Ticket Triage System
  1) New ticket
  2) Import tickets from CSV
  3) List all tickets
  4) View ticket detail
  5) Update ticket status
  6) Export tickets to CSV
  7) Show summary metrics
  8) Delete ticket
  0) Exit
```

Try option **2** and point it at `data/sample_data.csv` to load eight
pre-written example tickets and see the classifier in action, then use
option **3** to see them listed with severity, team, and due date, or
option **7** for aggregate metrics.

## Running tests

```bash
pytest tests/
```

## How classification works

The program combines the ticket title and description, converts the text to
lowercase, and checks a few keyword rules. Critical words are checked first,
then high, medium, and low words. Team rules use simple `if` statements. If
nothing matches, the ticket uses low severity and the support team.

The CLI uses plain `print()` statements. `pytest` is used for the automated
tests, while the application itself uses Python's standard library.

## Design notes / assumptions

- SLA windows are configurable via the `SLA_HOURS` dict in `logic.py`.
- The SQLite file lives at `data/tickets.db` by default; delete it to reset
  the ticket store from scratch.
- CSV import treats each row as a new ticket, so imported IDs do not collide
  with IDs already in the database.
