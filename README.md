# Digital Evidence Triage Tool

A command-line Python utility for performing initial triage of digital evidence files.

The tool scans an evidence directory, collects file metadata, calculates SHA-256 hashes, analyzes supported text-based evidence for security-related indicators, assigns per-file risk scores, and generates structured CSV and JSON reports.

---

## Purpose

During the initial stage of a cybersecurity investigation, an analyst may need to review multiple evidence files to determine which files deserve further investigation.

Manually inspecting every file can be time-consuming and inconsistent.

The **Digital Evidence Triage Tool** automates part of this initial review by:

- Discovering files inside an evidence directory
- Collecting basic file metadata
- Calculating SHA-256 hashes for integrity identification
- Extracting IPv4 addresses from text-based evidence
- Detecting predefined security-related events
- Identifying repeated IP activity
- Assigning per-file risk scores and risk levels
- Producing persistent CSV and JSON reports
- Presenting an overall triage summary in the terminal

The tool is intended for **initial triage and prioritization**, not as a replacement for full digital forensic analysis or a SIEM platform.

---

## Key Features

### Evidence Discovery

The tool recursively scans the supplied evidence directory and records:

- File name
- File path
- File extension
- File size
- Last modification time
- SHA-256 hash

### SHA-256 Hashing

Each discovered file is hashed using SHA-256.

The hash provides a reproducible identifier for the file contents and can help an analyst detect whether evidence has changed between collections.

### Security Event Analysis

For supported text-based files (`.txt` and `.log`), the tool searches for predefined indicators including:

- Failed login events
- Authentication failures
- Warnings
- Errors
- Critical events
- Access-denied events

Event matching is case-insensitive.

### IP Address Analysis

IPv4 addresses are extracted from supported text files using regular expressions.

Repeated activity from the same IP address contributes to the risk assessment when the same address appears three or more times within an analyzed file.

### Risk Assessment

Each analyzed file receives:

- A numerical risk score
- A risk level
- Human-readable reasons explaining why the score was assigned

The available risk levels are:

| Score | Risk Level |
|------:|------------|
| 0–2 | LOW |
| 3–5 | MEDIUM |
| 6–9 | HIGH |
| 10+ | CRITICAL |

The current scoring rules are:

| Indicator | Score |
|---|---:|
| Failed login | +2 per event |
| Warning | +1 per event |
| Error | +2 per event |
| Critical event | +4 per event |
| Denied access | +1 per event |
| Repeated IP activity (3+ occurrences) | +2 |

These scores are heuristic triage rules designed for this project. They are not an industry-standard threat-scoring framework.

---

## Requirements

Before running the project, you need:

- Python 3
- `pip`
- A command-line terminal
- The dependencies listed in `requirements.txt`

The project uses Python standard-library modules including:

- `argparse`
- `csv`
- `datetime`
- `hashlib`
- `json`
- `os`
- `re`
- `collections`
- `dataclasses`

Third-party packages include:

- `rich` — formatted command-line output
- `pytest` — automated testing

Install the required packages with:

```bash
python -m pip install -r requirements.txt
```

---

## Project Structure

```text
DigitalEvidenceTriage/
│
├── data/
│   └── sample_evidence/
│       ├── authentication.log
│       ├── network.log
│       ├── normal_activity.log
│       ├── notes.txt
│       └── system.log
│
├── reports/
│   ├── evidence_report.csv
│   └── triage_summary.json
│
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── main.py
│   ├── models.py
│   ├── reporter.py
│   ├── risk.py
│   ├── scanner.py
│   └── utils.py
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_risk.py
│   ├── test_scanner.py
│   └── test_utils.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `main.py` | CLI entry point and application workflow |
| `models.py` | Data models for evidence files and triage results |
| `scanner.py` | Directory scanning, metadata collection, and SHA-256 hashing |
| `analyzer.py` | IP extraction and security-event detection |
| `risk.py` | Risk-score calculation and classification |
| `reporter.py` | CSV and JSON report generation |
| `utils.py` | Input-directory validation |

This modular design separates the major responsibilities of the application and makes individual components easier to maintain and test.

---

## How to Run

Run commands from the **project root directory**.

### Analyze the included sample evidence

```bash
python -m src.main data/sample_evidence
```

The evidence directory is a required positional argument.

### Analyze another directory

```bash
python -m src.main path/to/evidence
```

### Choose a custom report directory

Use the optional `--output` argument:

```bash
python -m src.main data/sample_evidence --output my_reports
```

If `--output` is not supplied, reports are written to:

```text
reports/
```

### Display CLI help

```bash
python -m src.main --help
```

---

## Example Output

Running:

```bash
python -m src.main data/sample_evidence
```

produces a terminal summary similar to:

```text
Digital Evidence Triage Summary

┌──────────────────┬──────────┐
│ Metric           │ Result   │
├──────────────────┼──────────┤
│ Files Scanned    │ 5        │
│ Overall Risk     │ CRITICAL │
│ Total Risk Score │ 21       │
│ Report Directory │ reports  │
└──────────────────┴──────────┘

Status
Triage completed successfully.
```

The exact score and risk level depend on the contents of the supplied evidence.

---

## Generated Reports

A successful run generates two persistent reports.

### `evidence_report.csv`

Contains detailed per-file triage information, including:

- File name and type
- Risk level
- Risk score
- Security-event counts
- Unique IP addresses
- File size
- Human-readable modification time
- SHA-256 hash
- File path
- Reasons for the assigned risk

This report is designed to help an analyst quickly identify evidence files that may deserve further investigation.

### `triage_summary.json`

Contains the overall triage result, including:

- Number of files scanned
- Total risk score
- Overall risk level
- Risk reasons

JSON output also makes the result easier to consume programmatically in future integrations.

---

## Input Validation and Error Handling

The application validates the supplied evidence directory before processing it.

It handles cases such as:

- Directory does not exist
- Supplied path is not a directory
- Evidence directory is empty
- Files cannot be accessed because of permission or operating-system errors

For example:

```bash
python -m src.main wrong_folder
```

returns a readable message such as:

```text
Error: Evidence directory 'wrong_folder' does not exist.
```

rather than terminating with an unhandled traceback.

If an individual file cannot be processed, the scanner reports a warning and continues processing other accessible files where possible.

---

## Testing

The project includes automated unit tests using `pytest`.

Run all tests from the project root with:

```bash
python -m pytest -v
```

The test suite currently covers:

- IPv4 address extraction
- Security-event detection
- LOW risk assessment
- CRITICAL risk assessment
- SHA-256 calculation
- Directory scanning
- Valid directory handling
- Missing directory handling
- Empty directory handling

Current test suite:

```text
9 passed
```

---

## Sample Evidence

The `data/sample_evidence/` directory contains generated demonstration data representing different types of activity.

It includes examples of:

- Successful authentication
- Failed login attempts
- Repeated IP activity
- Network warnings
- Application errors
- Critical service events
- Access-denied activity
- Normal system activity

The sample files are provided only to demonstrate and test the application. They do not contain real incident or personal data.

---

## Known Limitations

The current version intentionally keeps the analysis rules transparent and relatively simple.

Known limitations include:

- Content analysis is currently limited to `.txt` and `.log` files.
- Other discovered file types can be hashed and inventoried by the scanner, but the current analysis pipeline does not inspect their internal contents.
- IPv4 extraction uses pattern matching and does not currently validate that every numeric octet is within the valid `0–255` range.
- IPv6 addresses are not currently analyzed.
- Security-event detection is keyword-based and does not perform semantic or behavioral analysis.
- Event detection depends on the predefined phrases in the analyzer and may miss differently worded events.
- A matching phrase is counted at most once per event category on each line to prevent overlapping phrases from being double-counted.
- Repeated-IP scoring is based on occurrences within an individual analyzed file rather than correlation across the entire evidence collection.
- Risk scores are project-defined heuristics and should not be interpreted as standardized forensic or threat-severity ratings.
- SHA-256 hashing identifies file content but does not by itself prove chain of custody or evidence authenticity.
- The tool performs initial triage only; it does not replace professional forensic examination, malware analysis, SIEM correlation, or incident-response investigation.

These limitations are documented intentionally so that users understand exactly what conclusions the tool can and cannot support.

---

## Future Improvements

Possible future improvements include:

- IPv6 support
- Strict IPv4 validation
- CSV and JSON evidence-content analysis
- Cross-file IP correlation
- Configurable detection rules
- Configurable risk-scoring weights
- Timestamp normalization
- Additional forensic metadata
- SQLite report storage
- Threat-intelligence API integration
- Additional command-line filtering options
- More comprehensive automated tests

---

## Technologies Used

- Python
- `argparse`
- Regular expressions
- SHA-256 / `hashlib`
- CSV
- JSON
- Object-oriented data models
- Rich
- pytest
- Git
- GitHub

---

## Design Approach

The application combines object-oriented data modeling with modular functional components.

`EvidenceFile` represents metadata collected from a discovered file, while `TriageResult` represents the security-analysis result associated with that evidence.

Scanning, analysis, risk calculation, reporting, and validation are separated into individual modules. This keeps the application easier to understand, test, and extend.

---

## Disclaimer

This project is an educational cybersecurity triage utility.

Its findings should be treated as indicators for further investigation rather than definitive evidence that malicious activity has occurred.