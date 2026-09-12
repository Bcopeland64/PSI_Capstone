# Cybersecurity Incident Triage Tool

## Description

Cybersecurity Incident Triage Tool is a Python command-line application
that helps users record and prioritize cybersecurity incidents.

## Features

- Add cybersecurity incidents
- Validate user input
- Calculate incident priority
- Save incidents to a JSON file
- Load saved incidents
- Display incident summaries
- Check an external service using an HTTP request
- Handle file and network errors

## Technologies

- Python
- JSON
- Requests
- Object-Oriented Programming
- Command Line Interface

## Project Structure

```text
capstone_project/
├── data/
│   └── incidents.json
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── utils.py
│   └── logic.py
├── tests/
│   └── test_logic.py
├── .gitignore
├── requirements.txt
└── README.md