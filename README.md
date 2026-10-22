# Security Incident Triage Tool

## Python Intensive Final Assignment — Capstone

### Project Overview

The **Security Incident Triage Tool** is an end-to-end Python CLI application that automates the initial processing of security incident records.

The application accepts incident data from CSV, validates and cleans the data, creates object-oriented incident records, assigns a severity level using transparent rule-based scoring, stores the results in SQLite, provides search and listing functions, and exports stored results to CSV.

The project is intentionally designed to demonstrate the technical requirements of the Python Intensive Capstone.

---

## Requirements Coverage

| Assignment Requirement | Implementation |
|---|---|
| Modular code architecture | `main.py`, `models.py`, `logic.py`, `utils.py`, `data_handler.py` |
| OOP / functional paradigm | `Incident`, `TriageEngine`, `DataHandler` classes |
| Data persistence | SQLite database |
| External file handling | CSV input and CSV report export |
| Error handling | `try/except`, validation errors, file/database errors |
| Input validation | Required fields, IP addresses, timestamps, IDs, CLI choices |
| External package integration | Pandas and Rich |
| Testing | Pytest unit tests |
| Clean/readable code | PEP 8-oriented structure and naming |
| Documentation | Docstrings and this README |

---

## Features

1. Import incident records from CSV.
2. Validate required fields.
3. Validate IPv4 and IPv6 addresses.
4. Validate timestamps.
5. Apply a transparent attack-type scoring rule.
6. Convert scores to LOW, MEDIUM, HIGH, or CRITICAL.
7. Store incidents persistently in SQLite.
8. Search for a specific incident.
9. List stored incidents.
10. Export stored incidents to CSV.
11. Handle invalid records without terminating the entire import.
12. Run automated unit tests.

---

## Triage Rules

The application uses a configurable rule table in `src/logic.py`:

| Attack Type | Score | Severity |
|---|---:|---|
| Port Scan | 1 | LOW |
| Brute Force | 2 | LOW |
| Phishing | 3 | MEDIUM |
| SQL Injection | 4 | HIGH |
| Malware | 5 | CRITICAL |
| Unknown attack type | 1 | LOW |

These values are **application rules for demonstration**, not a real-world incident-response standard.

---

## Project Structure

```text
capstone_project/
├── data/
│   └── sample_incidents.csv
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── logic.py
│   ├── data_handler.py
│   └── utils.py
├── tests/
│   ├── test_logic.py
│   └── test_data_handler.py
├── .gitignore
├── requirements.txt
└── README.md
```

The SQLite database and generated CSV report are created automatically when the application runs.

---

## Installation

### 1. Open a terminal in the project directory

```bash
cd capstone_project
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows Command Prompt:

```bash
venv\Scripts\activate
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Run the Application

From the project root:

```bash
python -m src.main
```

You should see:

```text
Security Incident Triage Tool

Menu

1. Process CSV incidents
2. Search incident
3. List stored incidents
4. Export stored incidents to CSV
5. Exit
```

Select option `1` to process the included sample dataset.

Press Enter when asked for the CSV path to use:

```text
data/sample_incidents.csv
```

---

## Database

The application creates:

```text
data/triage.db
```

The database contains an `incidents` table with:

- incident ID
- timestamp
- source IP
- destination IP
- attack type
- username
- description
- severity
- score

The database file is ignored by Git because it is generated application state.

---

## Export

Select option `4` to export the stored incidents.

The default output is:

```text
data/triage_report.csv
```

---

## Testing

Run all tests from the project root:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

The tests cover:

- Severity classification
- Attack scoring
- Invalid IP validation
- Invalid timestamp validation
- Unknown attack handling
- SQLite persistence
- Incident retrieval

---

## Error Handling

The application handles common failures including:

- Missing CSV files
- Empty CSV files
- Malformed CSV files
- Missing required fields
- Invalid IP addresses
- Invalid timestamps
- Invalid incident IDs
- Invalid menu selections
- Database/file-system errors

Invalid CSV records are reported and skipped while valid records continue through the pipeline.

---

## End-to-End Workflow

```text
CSV Input
    |
    v
Pandas DataFrame
    |
    v
Required Field Validation
    |
    v
IP + Timestamp Validation
    |
    v
Incident Object Creation
    |
    v
Rule-Based Triage Scoring
    |
    v
Severity Classification
    |
    v
SQLite Persistence
    |
    +------> Search
    |
    +------> List
    |
    +------> Statistics
    |
    +------> CSV Export
```

---

## Technologies Used

- Python 3
- Pandas
- Rich
- SQLite3
- Pytest
- CSV
- Dataclasses
- Object-Oriented Programming

`sqlite3`, `csv`, `ipaddress`, `datetime`, and other core functionality use Python's standard library.

Pandas, Rich, and Pytest are third-party packages.

---

## Design Decisions

### Modular Architecture

Responsibilities are separated into modules:

- `models.py` — data representation
- `logic.py` — triage/business logic
- `utils.py` — validation and utility functions
- `data_handler.py` — CSV and SQLite persistence
- `main.py` — CLI and application flow

### Object-Oriented Programming

The application uses custom classes to encapsulate state and behavior.

`Incident` represents an individual security event.

`TriageEngine` performs validation, scoring, and classification.

`DataHandler` manages persistent storage and data input/output.

### Persistence

SQLite was selected because it is a relational database included with Python and requires no separate database server.

### Third-Party Integration

Pandas provides reliable tabular CSV ingestion and data handling.

Rich improves CLI readability with formatted tables and panels.

Pytest provides automated testing.

---

## Limitations

This is an educational capstone application. The triage scoring rules are simplified and should not be treated as a production SOC decision engine.

The application does not:

- Perform live network monitoring.
- Execute attacks.
- Automatically block IP addresses.
- Claim that an incident is malicious solely from an attack-type label.
- Replace a professional incident-response process.

---

## Possible Future Enhancements

- REST API ingestion
- JSON ingestion
- Authentication and role-based access
- SIEM integration
- Automated alerting
- Configurable scoring rules
- PDF report generation
- Dashboard interface
- Log-file ingestion
- More extensive test coverage

---

## Author

Python Intensive Workshop Capstone Project.
