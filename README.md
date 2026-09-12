# Security Triage Script - Capstone Project

This project is a simple command-line triage tool built in Python. It collects running processes, calculates the SHA-256 hash of a file, and checks a network log for common and suspicious ports.

## What the Script Does
- Takes a sample of running processes using psutil (or system commands if not installed).
- Calculates the SHA-256 hash to check file integrity.
- Reads a CSV file of network logs to count the top destination ports and flag suspicious ports like 4444.
- Exports the summary results to triage_summary.csv.

## Project Structure
- data/sample_data.csv: Sample traffic logs used for testing.
- src/logic.py: Contains the main SecurityTriage class and analysis functions.
- src/utils.py: Helper functions for file validation and CSV export.
- src/main.py: The entry point that runs the full triage step by step.
- tests/test_logic.py: A basic unit test to verify the hashing logic.
- requirements.txt: Project dependencies.

## Setup and Installation

1. Create and activate a virtual environment:
    python -m venv .venv
    .venv\Scripts\activate

2. Install the required libraries:
    pip install -r requirements.txt

## How to Run

Run the triage tool:
    python src/main.py data/sample_data.csv

Run the unit test:
    python -m unittest tests/test_logic.py