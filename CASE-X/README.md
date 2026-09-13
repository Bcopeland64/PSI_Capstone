# CASE-X

**CASE-X — Intelligent Criminal Investigation & Evidence Analysis System**

A Python capstone project that demonstrates modular programming, OOP/data modeling, SQLite persistence, input validation, error handling, third-party libraries, reporting, and unit testing.

> This is an educational simulation. The suspicion score is a transparent demo heuristic, not a real-world forensic or law-enforcement method.

## Features

- Create and browse investigation cases.
- Add suspects and alibis.
- Add evidence with a reliability score.
- Link evidence to suspects.
- Rank suspects using an explainable scoring heuristic.
- Persistent SQLite database.
- Interactive terminal UI using Rich.
- Export suspect rankings to CSV with Pandas.
- Generate a score chart with Matplotlib.
- Unit test for the core ranking logic.

## Project structure

```text
CASE-X/
├── data/
│   └── sample_data.csv
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── logic.py
│   ├── main.py
│   ├── models.py
│   ├── reporting.py
│   └── utils.py
├── tests/
│   └── test_logic.py
├── reports/
├── .gitignore
├── requirements.txt
└── README.md
```

## Run

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start:

```bash
python -m src.main
```

Run tests:

```bash
pytest
```

## Scoring idea

For each suspect, CASE-X considers the reliability of linked evidence and the number of distinct evidence items. The formula is deliberately simple and explainable so it can be presented during the capstone evaluation.

## Future improvements

- User authentication and investigator roles.
- Evidence timeline.
- Advanced search and filters.
- PDF report generation.
- Web dashboard with Flask/FastAPI.
- More rigorous scoring models.
