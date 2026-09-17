# NetLogSec 🛡️

**NetLogSec** is a modular Python-based network security and log analysis utility designed to parse security logs, detect brute-force attacks using rolling time windows, and generate detailed threat reports. 

Developed as a cybersecurity capstone project, it demonstrates clean architecture, Object-Oriented Programming (OOP), data manipulation with Pandas, and robust error handling.

---

## 🚀 Features

* **Log Parsing & Regex:** Extracts timestamps, IP addresses, statuses, and usernames from raw log data.
* **Time-Window Brute-Force Detection:** Detects rapid consecutive failed login attempts within a specific rolling time window (e.g., 5 minutes).
* **Severity Scoring:** Automatically categorizes security alerts into `Medium` or `High` threat levels.
* **Input Validation:** Securely validates IPv4 and IPv6 addresses using Python's standard `ipaddress` library.
* **Automated Testing:** Comprehensive unit tests implemented using `pytest`.

---

## 📂 Project Structure

```text
net-log-sec/
├── data/
│   └── sample_auth.log        # Sample log dataset for testing
├── src/
│   ├── __init__.py
│   ├── main.py            # CLI entry point and user interaction
│   ├── logic.py           # Core log analysis and time-window rules
│   ├── models.py          # Data classes (SecurityAlert OOP structure)
│   └── utils.py           # Helper validation functions (IP, files)
├── tests/
│   └── test_logic.py      # Unit tests for validation and models
├── .gitignore             # Git ignore rules for cache & virtual environments
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation


🛠️ Installation & Setup
Clone the Repository:

Bash
git clone [https://github.com/AL-A9EL/net-log-sec.git](https://github.com/AL-A9EL/net-log-sec.git)
cd net-log-sec
Install Dependencies:

Bash
pip install -r requirements.txt

💻 Usage
Run the interactive Command Line Interface (CLI):

Bash
python -m src.main
CLI Menu Options:

1. Load and Parse Log File: Enter the path to your log file (e.g., data/sample_auth.log).
2. Detect Brute Force Attacks: Set your preferred time window (minutes) and failed attempts threshold to scan for threats.
3. Export Comprehensive Report: Save parsed logs into a structured CSV report.
4. Exit: Safely close the utility.

🧪 Running Unit Tests
To verify code integrity and run automated unit tests with pytest:

Bash
python -m pytest -v
👨‍💻 Author
Al-Asel Abdalla Twairesh
