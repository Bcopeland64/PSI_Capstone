# Security Alert Triage Script

A simple script that reads security alerts from a CSV file, sorts them by
severity level (Low/Medium/High/Critical), and saves the sorted result to a
JSON file.

## Structure
- `src/models.py` — Alert class (OOP)
- `src/utils.py` — file reading + input validation (error handling)
- `src/logic.py` — sorting logic + external API call
- `src/main.py` — entry point
- `data/alerts.csv` — sample data
- `tests/test_logic.py` — basic unit test

## Run
```bash
pip install -r requirements.txt
python src/main.py
```

## Requirements covered
- OOP: Alert class
- Data persistence: reading CSV + writing JSON
- Error handling: try/except around file reading and the API call
- External package: requests
- Modular structure: 4 separate files, each with a single responsibility
