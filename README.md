# DFIR Triage Automation Tool (Capstone Project)

## Project Overview
This project is an end-to-end Digital Forensics and Incident Response (DFIR) triage application. It is designed to scan a target directory, identify recently modified files, calculate their SHA-256 cryptographic hashes, and sample running processes. The final intelligence is exported to a structured JSON report for further analysis.

## Key Features
* **Modular Architecture:** Clean separation of concerns (`main.py`, `logic.py`, `utils.py`).
* **Object-Oriented Programming (OOP):** Core logic is encapsulated within the `TriageScanner` class.
* **Data Persistence:** Automatically exports findings to `data/triage_report.json`.
* **Error Handling & Validation:** Robust exception handling for missing files, permission errors, and invalid user inputs.

## Repository Structure
```text
capstone_project/
├── data/
│   ├── sample_evidence/
│   └── triage_report.json
├── src/
│   ├── __init__.py
│   ├── logic.py
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_logic.py
├── .gitignore
├── requirements.txt
└── README.md