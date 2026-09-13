# Security Alert Triage CLI

A command-line tool that reads raw security alerts (failed logins, root
login attempts, privilege escalation events) from a CSV file, classifies
each one by severity, groups activity by source IP, and exports a JSON
triage report, automating the first-pass triage a SOC analyst does
before deeper investigation.

## Features

- **Functional design**: alerts and summaries are plain dictionaries;
  behavior lives in small, focused functions rather than classes.
- **Data persistence**: reads CSV input, writes a JSON report.
- **Validation & error handling**: invalid CSV rows are skipped (with a
  printed warning) instead of crashing the program; a missing input file
  raises a clear error instead of a traceback.
- **Tests**: `pytest` unit tests cover the severity classification rules.

## Project Structure

```
PSI_Capstone/
├── data/
│   └── sample_alerts.csv
├── src/
│   ├── __init__.py
│   ├── main.py       # CLI entry point (the menu loop)
│   ├── models.py     # alert/summary dicts + classify_alert()
│   ├── logic.py      # load_alerts(), summarize_by_source(), export_report()
│   └── utils.py      # validate_row(), is_valid_ip()
├── tests/
│   └── test_logic.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/dinaabdulhadi/PSI_Capstone.git
cd PSI_Capstone

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

Run the CLI from the project root (the folder containing `src/`):

```bash
python -m src.main
```

Menu options:
1. **Load and triage alerts**: reads `data/sample_alerts.csv`, validates
   each row, and classifies every alert's severity.
2. **View summary by source IP**: prints alerts grouped by IP, showing
   total failed attempts, event types seen, and the worst severity found.
3. **Export report to JSON** :saves the grouped summary to `data/report.json`.
4. **Exit**

## Running Tests

```bash
python -m pytest tests/ -v
```

## Severity Rules

| Condition                                              | Severity |
|-----------------------------------------------------------|----------|
| `event_type` is "privilege escalation"                     | CRITICAL |
| `event_type` is "root login attempt" with 2+ failed attempts | CRITICAL |
| `event_type` is "root login attempt" with 0–1 failed attempts | HIGH     |
| 10+ failed attempts (any other event type)                 | CRITICAL |
| 5–9 failed attempts                                        | HIGH     |
| 1–4 failed attempts                                        | MEDIUM   |
| 0 failed attempts (e.g. a successful login)                | LOW      |

Privilege escalation is always treated as critical since there's rarely a
routine reason for it to occur. Root login attempts start at HIGH rather
than CRITICAL, since a single attempt could be a legitimate admin, repeated
attempts are what start to look like guessing.

## License

MIT
