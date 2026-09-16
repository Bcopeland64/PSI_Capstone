# End-to-End Security Triage Script

## Python Workshop Capstone Project

### 1. Project Overview

The End-to-End Security Triage Script is a Python command-line application for basic cybersecurity log triage.

It reads SSH authentication logs, identifies successful and failed authentication events, counts failed attempts by source IP, flags IP addresses that reach a configurable threshold, and generates persistent JSON and CSV reports.

The project demonstrates Python programming, modular architecture, Object-Oriented Programming, data handling, validation, error handling, third-party package integration, and automated testing.

### 2. Real-World Problem

Security analysts frequently review authentication logs to identify unusual login activity. Manually counting repeated failed login attempts can be slow and error-prone.

This application automates the first stage of that review by:

- Parsing authentication log entries.
- Counting failed and successful logins.
- Identifying source IP addresses.
- Flagging IP addresses with repeated failed attempts.
- Exporting structured reports for further investigation.

A flagged IP is an investigation indicator, not proof of malicious activity.

### 3. Technical Requirements Covered

| Requirement | Implementation |
|---|---|
| Modular architecture | `main.py`, `models.py`, `logic.py`, `utils.py`, `data_handler.py` |
| OOP | `LogAnalyzer`, `LogEvent`, `TriageResult` |
| Data persistence | JSON and CSV reports |
| Error handling | `try/except` in CLI workflow |
| Input validation | File path and threshold validation |
| External packages | Pandas and Rich |
| Unit testing | Pytest |
| Documentation | README and Python docstrings |
| Clean structure | PEP 8-oriented naming and organization |

### 4. Project Structure

```text
capstone_project/
├── data/
│   └── sample_auth.log
├── reports/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── utils.py
│   ├── logic.py
│   └── data_handler.py
├── tests/
│   └── test_logic.py
├── .gitignore
├── requirements.txt
└── README.md
```

### 5. Installation

Requirements:

- Python 3.10+
- pip

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 6. Run the Application

Run the included sample log:

```bash
python -m src.main
```

Use a custom threshold:

```bash
python -m src.main data/sample_auth.log --threshold 3
```

Specify another report path:

```bash
python -m src.main data/sample_auth.log --threshold 5 --output reports/my_report.json
```

### 7. Generated Reports

The application generates:

- JSON summary report.
- CSV file containing parsed events.
- CSV file containing summary metrics.

Example output files:

```text
reports/triage_report.json
reports/triage_report_events.csv
reports/triage_report_summary.csv
```

### 8. Testing

Run the automated tests:

```bash
pytest
```

The tests verify:

- Failed login parsing.
- Successful login parsing.
- Suspicious IP threshold detection.

### 9. Example Result

With the included sample data and a threshold of 5, the application identifies repeated failed attempts from:

```text
192.168.1.50  -> 5 failed attempts
10.0.0.25     -> 5 failed attempts
172.16.0.15   -> 5 failed attempts
```

The sample contains:

```text
Total events       : 19
Failed logins      : 15
Successful logins  : 3
Other events       : 1
Unique IPs         : 6
Suspicious events  : 15
```

### 10. OOP Design

`LogAnalyzer` encapsulates the main analysis state and methods.

`LogEvent` represents a parsed event.

`TriageResult` represents the final analysis result.

This separation makes the application easier to maintain and extend.

### 11. Error Handling

The application handles:

- Missing log files.
- Unreadable files.
- Empty paths.
- Empty log files.
- Invalid threshold values.
- Threshold values below 1.
- General file-system errors.

Instead of crashing with an unhandled exception, the CLI reports a readable error message.

### 12. External Package Integration

**Pandas** is used to convert parsed event data into structured CSV reports.

**Rich** is used to display readable terminal tables.

**Pytest** is used for automated unit testing.

### 13. Security Considerations

The application is intentionally designed as a basic triage tool.

Repeated failed authentication attempts may indicate password guessing, credential attacks, misconfiguration, or legitimate user error. The program therefore flags events for analyst review rather than automatically classifying them as attacks.

### 14. Limitations

This educational project does not replace a SIEM, EDR, IDS, or professional DFIR platform.

A production implementation would normally include:

- Centralized log collection.
- Time-zone normalization.
- Correlation across multiple log sources.
- User and asset context.
- Threat-intelligence enrichment.
- Alert severity scoring.
- Database storage.
- Authentication and access controls.

### 15. Future Improvements

Possible extensions include:

- SQLite database support.
- Additional log formats.
- Interactive menu mode.
- IP geolocation through an approved API.
- Visualization using Matplotlib.
- Export to HTML.
- More extensive test coverage.

## Author

Python Workshop Capstone Project
