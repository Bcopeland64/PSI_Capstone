# Security Triage Tool

A modular Python command-line utility designed for basic security triage operations, network traffic parsing, and artifact integrity verification.

## Features

- **File Integrity Checking**: Computes SHA-256 hashes of local files for integrity validation.
- **Port Scanner**: Performs quick TCP banner/port checks using non-blocking socket operations.
- **Traffic Analysis**: Parses CSV network connection logs using Python's `Counter` to identify top talkers by byte volume.
- **Reporting**: Automatically exports analysis summaries to text reports.

## Project Structure

```text
PROJECT ON PYTHON/
│
├── data/
│   ├── sample_data.csv       # Sample network connection dataset
│   └── report.txt            # Generated triage reports
│
├── src/
│   ├── __init__.py           # Package marker
│   ├── main.py               # Application entry point & interactive CLI
│   ├── utils.py              # Low-level utilities (hashing, scanning, API calls)
│   └── logic.py              # Parsing logic & persistence
│
├── requirements.txt          # Third-party dependencies
└── README.md                 # Project documentation