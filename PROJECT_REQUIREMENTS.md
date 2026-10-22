# Capstone Requirements Checklist

This file maps the submitted project directly to the assignment requirements.

## Required Technical Components

### 1. Modular Code Architecture
Implemented through:
- `src/main.py`
- `src/models.py`
- `src/logic.py`
- `src/utils.py`
- `src/data_handler.py`

### 2. OOP or Functional Paradigm
Implemented with:
- `Incident`
- `TriageEngine`
- `DataHandler`

### 3. Data Persistence
Implemented using SQLite:
- `data/triage.db`

The application also reads and writes CSV files.

### 4. Error Handling and Input Validation
Implemented using:
- `try/except`
- required-field validation
- IP address validation
- timestamp validation
- incident ID validation
- CLI input validation
- CSV and database error handling

### 5. External Package / API Integration
Third-party packages:
- Pandas
- Rich
- Pytest

No external web API is required by the assignment; the external-package requirement is satisfied through these packages.

### 6. Clean and Readable Code
Implemented through:
- descriptive names
- module separation
- docstrings
- type hints
- PEP 8-oriented formatting
- concise comments and documentation

## Repository Structure

The repository includes:
- `data/`
- `src/`
- `tests/`
- `.gitignore`
- `requirements.txt`
- `README.md`

## Testing

Run:

```bash
pytest -v
```

## Application

Run:

```bash
python -m src.main
```
