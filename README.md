# Cybersecurity Log Analyzer

A simple Python-based cybersecurity log analysis tool.

The project reads log files, analyzes IP address activity and error events, stores the results in CSV format, and generates a visual report.

## Features

* Read cybersecurity log files
* Count log events by IP address
* Count `ERROR` events
* Validate input log files
* Handle missing and invalid files
* Store analysis results in CSV format
* Generate a bar chart
* Object-Oriented Programming
* Unit testing with pytest

## Project Structure

```text
cyber-log-analyzer/
│
├── data/
│   ├── sample.log
│   ├── report.csv
│   └── ip_activity.png
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── analyzer.py
│   └── utils.py
│
├── tests/
│   └── test_analyzer.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies

* Python
* Pandas
* Matplotlib
* Pytest

## Installation

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python src/main.py
```

The analyzer will process the sample log file and generate:

* `data/report.csv`
* `data/ip_activity.png`

## Testing

Run the unit tests:

```bash
python -m pytest
```

## Example Output

```text
=== Cybersecurity Log Analyzer ===
Total log lines: 6
Total errors: 2

IP Address Activity:
192.168.1.10: 2 events
10.0.0.5: 3 events
192.168.1.20: 1 event

Report saved to data/report.csv
Graph saved to data/ip_activity.png
```

## Learning Objectives

This project demonstrates:

* Python functions
* Object-Oriented Programming
* File handling
* Exception handling
* Input validation
* Data processing
* Pandas
* Matplotlib
* Unit testing
* Modular project structure

## Disclaimer

This project is intended for educational purposes and analyzes sample log data only.
