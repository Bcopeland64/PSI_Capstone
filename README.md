# Task & Inventory Management System

A Python-based inventory and task management application that helps small businesses or students track stock, monitor low inventory, and record inventory-related transactions.

## Features
- Add, update, search, and remove inventory items
- Track stock movements with transaction history
- Detect low-stock items based on reorder thresholds
- Save data to CSV files for persistence
- Generate simple inventory reports
- Built with OOP design and input validation
- Includes a Rich-powered terminal interface

## Project Structure
- `src/main.py` – command-line interface
- `src/logic.py` – core inventory logic and business rules
- `src/models.py` – item and transaction dataclasses
- `src/data_handler.py` – CSV read/write functions
- `src/utils.py` – validation and formatting helpers
- `tests/test_logic.py` – unit tests



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
