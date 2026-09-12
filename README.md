<<<<<<< HEAD
# 🕵️‍♂️ DFIR End-to-End Triage

### Digital Forensics & Incident Response Project

---

## 📌 Overview

This project is a Python-based **Digital Forensics & Incident Response (DFIR)** tool designed to perform an end-to-end triage on a target system or evidence folder.

The tool collects and analyzes running processes, file evidence, duplicate files, forensic artifacts from CSV logs, network port status, system command output, and HTTP responses. It then generates a structured JSON report and a visualization of artifact activity.

The project demonstrates modular Python development, data handling, error handling, external package usage, and practical cybersecurity-oriented analysis.

---

## ⚙️ Features

- 🔍 **Process Analysis** → Lists running processes with their PID and name.
- 📂 **File Evidence** → Extracts file size, modification time, SHA-256 hash, and recent-file status.
- 🧩 **Duplicate Detection** → Identifies duplicate files by comparing SHA-256 hashes.
- 📊 **Artifact Analysis** → Reads forensic events from a CSV file and calculates statistics by event type and hour.
- 📈 **Visualization** → Generates a stacked bar chart showing artifact events by type and hour.
- 🌐 **Network Checks** → Checks whether a specific TCP port is open on a target host.
- 💻 **System Commands** → Runs a system command such as `whoami` to provide system context.
- 🌍 **HTTP Requests** → Checks HTTP responses from test URLs.
- 📝 **Final Report** → Combines the collected results into a JSON report.

---

## 📁 Project Structure

```text
DFIR Triage Tool/
│
├── data/
│   ├── artifacts.csv
│   └── sample_evidence/
│       ├── notes.txt
│       ├── payload.pin
│       └── report.docx
│
├── reports/
│   ├── artifact_stacked.png
│   └── triage_report.json
│
├── src/
│   ├── __init__.py
│   ├── data_handler.py
│   ├── logic.py
│   ├── main.py
│   ├── models.py
│   └── utils.py
│
├── tests/
│   └── test_logic.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

### Main Modules

| File | Purpose |
|---|---|
| `src/main.py` | Main entry point and end-to-end triage workflow |
| `src/logic.py` | Process, file, hash, duplicate, port, command, and HTTP checks |
| `src/data_handler.py` | CSV reading, artifact analysis, and JSON report writing |
| `src/models.py` | Data classes used to represent evidence and process information |
| `src/utils.py` | Helper functions and input validation |
| `tests/test_logic.py` | Unit tests for core logic |

---

## 🚀 How to Run

### 1️⃣ Install Python

Make sure **Python 3.9 or newer** is installed.

Check your Python version:

```bash
python --version
```

### 2️⃣ Install Dependencies

Install the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

The project uses:

- `psutil` → Process and system information
- `requests` → HTTP requests
- `matplotlib` → Data visualization
- `pytest` → Unit testing

### 3️⃣ Run the Tool

Because the project uses package-relative imports, run the application from the project root with:

```bash
python -m src.main data/sample_evidence data/artifacts.csv
```

> **Important:** Use `python -m src.main` instead of `python src/main.py` so the relative imports inside the `src` package work correctly.

### 4️⃣ Generated Outputs

After the tool finishes, the following files are generated or updated:

```text
reports/
├── triage_report.json
└── artifact_stacked.png
```

---

## 📊 Example Visualization

The generated stacked bar chart shows the number of forensic events grouped by hour and divided by event type.

For the provided sample dataset:

```text
08:00 → 9 events
09:00 → 4 events
10:00 → 7 events
11:00 → 3 events
```

The chart separates events into:

- `process_started`
- `file_created`
- `file_deleted`

This makes it easier to identify periods with higher activity during triage.

---

## 📄 Example Report

The tool generates `reports/triage_report.json` containing information such as:

```json
{
    "target_folder": "data/sample_evidence",
    "generated_at": "Sat Sep 12 05:49:00 2026",
    "process_count": 10,
    "file_count": 3,
    "recent_files": [],
    "duplicate_files": {},
    "artifact_analysis": {
        "total_events": 23,
        "by_type": {
            "process_started": 8,
            "file_created": 8,
            "file_deleted": 7
        },
        "by_hour": {
            "08": 9,
            "09": 4,
            "10": 7,
            "11": 3
        }
    },
    "port_80_open": false,
    "whoami": "example_user",
    "http_checks": {
        "https://httpbin.org/status/200": 200,
        "https://httpbin.org/status/403": 403,
        "https://httpbin.org/status/404": 404
    }
}
```

Some values, such as the process count, username, port status, and generated timestamp, depend on the machine where the tool is executed.

---

## 🧪 Running Tests

The project includes unit tests for core functionality.

Run the tests with:

```bash
python -m pytest
```

The tests cover functions such as file hashing and duplicate-file detection.

---

## 📌 Sample Evidence

The `data/sample_evidence/` folder contains sample files used to demonstrate the file-analysis functionality:

- `notes.txt` → Sample investigator notes.
- `payload.pin` → Sample evidence file used for hashing and file analysis.
- `report.docx` → Sample evidence file included in the evidence folder.
- `artifacts.csv` → Structured forensic event data used for artifact analysis.

These files are provided as **sample evidence for the project demonstration** and are not intended to represent a real incident.

---

## 🛡️ Error Handling

The application includes error handling for common situations such as:

- Missing evidence folders
- Missing artifact CSV files
- File access errors
- Process access errors
- HTTP request failures
- System command failures

This allows the tool to continue gracefully when certain information cannot be collected.

---

## 🏗️ Technical Requirements Demonstrated

This project demonstrates the main requirements of the Python Workshop Capstone:

- ✅ Modular code architecture
- ✅ Python functions and data classes
- ✅ File-based data persistence
- ✅ CSV data processing
- ✅ JSON report generation
- ✅ Error handling with `try/except`
- ✅ Input validation
- ✅ Third-party package integration
- ✅ Data visualization with Matplotlib
- ✅ Unit testing with Pytest
- ✅ Clean and documented Python code

---

## 🏁 Conclusion

The **DFIR End-to-End Triage** project provides a practical Python workflow for collecting evidence, analyzing forensic data, checking system and network information, visualizing activity, and generating a structured report.

It combines Python programming fundamentals with a real-world cybersecurity use case and demonstrates an end-to-end approach to digital forensics and incident response triage.
=======
# 🚀 Python Workshop: Capstone Project

Welcome to the **Python Workshop Capstone Project**! This project serves as the final, comprehensive assessment of your journey through the workshop. It is designed to combine core programming fundamentals with practical software development workflows, problem-solving, and data handling.

---

## 📌 Project Overview

For this capstone, students are required to design, build, and document a fully functional Python application. The project must solve a real-world problem or streamline a business process, demonstrating mastery of the core Python concepts covered throughout the workshop.

### 💡 Project Ideas & Scope
You may choose one of the following tracks or propose a custom project (subject to instructor approval):
1. **Data Analytics & Automation Pipeline**: Fetch data from an external API or dynamic CSV/JSON dataset, perform data cleaning and transformation using Pandas, and generate automated visual reports/summaries.
2. **Interactive CLI / Utility Tool**: Build an interactive Command Line Interface (CLI) application with persistent data storage (SQLite or file-based JSON/CSV), robust user input validation, and modular structure.
3. **Web Scraper & Analysis Tool**: Construct an ethical web scraping tool (using `BeautifulSoup` or `requests`), parse and store structured data, and output insights/metrics to the user.
4. **Task/Inventory Management System**: Develop an Object-Oriented Programming (OOP) system managing entities, state, transactions, and historical reporting.

---

## 🛠️ Required Technical Components

To pass the capstone project, your codebase **must** incorporate the following elements:

* **Modular Code Architecture**: Clear organization across separate modules/files (e.g., `main.py`, `models.py`, `utils.py`, `data_handler.py`).
* **Object-Oriented Programming (OOP)** or Functional Paradigms: Effective use of custom classes, methods, encapsulated state, or pure functional structures.
* **Data Persistence**: Ability to read from and write to external files (`.csv`, `.json`, `.txt`) or a relational database (`SQLite`).
* **Error Handling & Input Validation**: Implementation of `try-except` blocks to handle edge cases, missing files, API rate limits, and invalid user inputs gracefully.
* **External Package / API Integration**: Utilization of standard libraries alongside third-party modules (e.g., `requests`, `pandas`, `matplotlib`, `rich`, or `pytest`).
* **Clean & Readable Code**: PEP 8 compliance, informative variable/function naming, concise comments, and explicit docstrings for major functions/classes.

---

## 📂 Repository Structure

Your final submission repository should adhere to a clean layout similar to this:

```text
capstone_project/
├── data/                  # Sample or generated datasets (CSV, JSON, DB)
│   └── sample_data.csv
├── src/                   # Core application source code
│   ├── __init__.py
│   ├── main.py            # Main entry point for running the application
│   ├── utils.py           # Helper functions and validations
│   └── logic.py           # Main business/data processing logic
├── tests/                 # Unit tests (optional/extra credit)
│   └── test_logic.py
├── .gitignore             # Git ignore file for __pycache__, envs, etc.
├── requirements.txt       # List of Python dependencies
└── README.md              # Project documentation and setup instructions
>>>>>>> 1738576ca10037fe1450c351712fd0e1c2fa11ea
