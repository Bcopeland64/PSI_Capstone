


# Forensic & Network Triage CLI Tool

A modular, OOP-based Python Incident Response CLI application designed to automate host network probing, filesystem metadata collection, and cryptographic SHA-256 artifact hashing.

## Features
* **Modular Architecture**: Separate modules for utilities (`utils.py`), business logic (`logic.py`), and CLI entry (`main.py`).
* **OOP Paradigms**: `TriageScanner` class handles all system interactions and state.
* **Error Handling**: Graceful exception catches for socket timeouts and missing files.
* **Data Persistence**: Automatic export of triage artifacts to JSON (`data/triage_report.json`).

## Execution
Run the entry point from the project root:
```bash
python src/main.py