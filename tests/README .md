# Security Log Analyzer

## Project Description

Security Log Analyzer is a Python application that analyzes security log files and counts INFO, WARNING, and ERROR events.

The project is designed to help identify login activity and failed login attempts from security logs.

## Features

- Reads security logs from an external text file.
- Counts INFO, WARNING, and ERROR log entries.
- Saves analysis results to an external file.
- Validates user input.
- Handles missing files and file errors.
- Checks internet connectivity using the requests library.
- Uses Object-Oriented Programming.
- Includes automated tests using pytest.
- Uses modular Python files for better organization.

## Project Structure

```text
security_log_analyzer/
│
├── data/
│   ├── sample_data.txt
│   └── analysis_results.txt
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── logic.py
│   ├── utils.py
│   └── data_handler.py
│
├── tests/
│   └── test_logic.py
│
├── .gitignore
├── requirements.txt
└── README.md

Requirements
• Python 3
• requests
• pytest
Install the required packages with:
pip install -r requirements.txt

How to Run
From the project folder, run:
python src/main.py
When prompted for the log file path, enter:
data/sample_data.txt
The application will analyze the logs and save the results to:
data/analysis_results.txt

Testing
Run the automated tests with:
pytest

Example Output
Log Analysis Results:
INFO: 3
WARNING: 1
ERROR: 3

Error Handling
The application handles:
• Empty file paths.
• Missing log files.
• File reading errors.
• Invalid log levels.
• Network connection errors.

Technologies
• Python
• Object-Oriented Programming
• Requests
• Pytest
• Git
