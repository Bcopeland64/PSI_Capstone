# Data Analytics & Log Processing Automation Pipeline

This project is an Automated Log Analytics and Data Processing Pipeline written in Python. It ingests system/security access logs from a CSV file, cleans and processes the data using Pandas, generates statistical JSON summaries, and produces visual reports with Matplotlib.

--- 

## Features

- **Data Ingestion & Cleaning**: Reads log files using Pandas and cleans whitespace or missing values.
- **Statistical Analytics**: Analyzes event distributions and identifies top frequent paths/actions.
- **JSON Data Persistence**: Exports key analytics metrics directly to `summary_report.json`.
- **Automated Visualization**: Generates a bar chart distribution saved as `events_chart.png`.
- **Modular OOP Architecture**: Built using Object-Oriented Principles with the `DataPipeline` class for clean code structure.

---

## Repository Structure

```text
capstone_project/
├── data/
│   ├── events_chart.png       # Generated visualization chart
│   ├── sample_evidence.csv    # Input log dataset
│   └── summary_report.json    # Exported summary metrics
├── src/
│   ├── __init__.py
│   ├── logic.py               # DataPipeline class & business logic
│   ├── main.py                # Main application entry point
│   └── utils.py               # Helper functions & file operations
├── .gitignore
├── README.md                  # Project documentation
└── requirements.txt           # External Python dependencies