# Security Triage Tool

## Overview

The Security Triage Tool is a Python-based security utility designed to collect and analyze system information for basic security triage.

The tool collects process information, identifies processes that may require review, finds recently modified files, calculates SHA-256 hashes, and generates a security report.

## Features

* Collect running process information
* Analyze processes for suspicious indicators
* Identify processes that require review
* Find recently modified files
* Calculate SHA-256 file hashes
* Generate a security triage report
* Run automated unit tests

## Project Structure

```text
security-triage-tool-Yaqeen-cancon/
├── data/
│   ├── sample_data.csv
│   └── test.log
├── reports/
│   └── process_report.txt
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
│   └── logic.py
├── tests/
│   └── test_logic.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.13+
* psutil
* pytest

## Setup

Create and activate the virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Run the Tool

Run the main application with:

```bash
python -m src.main
```

The generated report is saved to:

```text
reports/process_report.txt
```

## Run Tests

Run the automated tests with:

```bash
python -m pytest
```

## Security Note

A process marked as `REVIEW` is not automatically malicious. It means that the process contains an indicator that should be reviewed manually.
