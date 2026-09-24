# Cybersecurity Triage Tool

## Project Overview
The Cybersecurity Triage Tool is an interactive Python CLI application designed to help a user perform a basic first-level triage of suspicious files.

The program collects security indicators, calculates a risk score, assigns a risk level, stores cases in JSON format, supports searching, and generates a summary report.

## Features
- Interactive command-line interface
- Object-Oriented Programming using `TriageCase`
- Risk scoring from security indicators
- LOW, MEDIUM, and HIGH risk classification
- JSON data persistence
- Search functionality
- Input validation
- Error handling for file operations
- Summary reporting
- Unit tests with pytest
- Modular project structure

## Requirements
- Python 3.10 or newer
- VS Code
- Optional: pytest for tests

## How to Run in VS Code

Open the project folder in VS Code.

Open the terminal and run:

```bash
python src/main.py
```

If your computer uses `python3`, run:

```bash
python3 src/main.py
```

## How to Run Tests

Install pytest:

```bash
pip install -r requirements.txt
```

Then run:

```bash
pytest
```

## Risk Scoring
- Executable file: +2
- Downloaded from Internet: +2
- Antivirus alert: +4
- Suspicious extension: +2

Maximum score: 10.

Risk levels:
- 0–3: LOW
- 4–6: MEDIUM
- 7–10: HIGH

## Data Storage
Cases are stored in:

`data/triage_cases.json`

The file is created and updated automatically.

## Educational Purpose
This project is intended for educational cybersecurity triage practice. It does not replace professional malware analysis or incident response tools.
