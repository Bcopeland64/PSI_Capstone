# End-to-End Cybersecurity Triage Script

## Purpose

This capstone is a small, read-only Python triage tool inspired directly by
the techniques practiced during the 3-day Python for Security workshop.

It collects:
- a sample of running processes;
- recently modified files;
- SHA-256 file hashes;
- a simple file timeline;
- a CSV report of the file findings.

## Workshop techniques used

The project uses the workshop's demonstrated techniques:
- functions and docstrings;
- `os`, `os.stat()`, and filesystem checks;
- `hashlib.sha256()`;
- file reading/writing;
- CSV output;
- loops, conditions, dictionaries and lists;
- `subprocess.run()` for a read-only process-listing fallback;
- `psutil` as the external package;
- command-line arguments with `argparse`;
- `try/except` error handling.

Day 1 focused on file handling, parsing, regular expressions, functions and
`Counter`. Day 2 added `requests`, CSV parsing, OS interaction, hashing and
safe local checks. Day 3 combined processes, file metadata, hashes, timelines
and reporting into the end-to-end triage workflow.

## Repository structure

```text
capstone_project/
├── data/
│   └── sample_evidence/
├── output/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── logic.py
│   ├── report.py
│   └── utils.py
├── tests/
│   └── test_logic.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- `psutil`

Install the dependency:

```bash
pip install -r requirements.txt
```

## How to run

From the project root:

```bash
python -m src.main data/sample_evidence
```

You can change the recent-file window:

```bash
python -m src.main data/sample_evidence --window 3600
```

You can choose a different CSV output path:

```bash
python -m src.main data/sample_evidence --output output/my_report.csv
```

## Error handling

The program checks whether the target is a valid directory and handles
invalid paths, permission errors and operating-system errors without
crashing with an unhandled traceback.

## Testing

Run:

```bash
python -m unittest discover -s tests -v
```

## Example output

```text
============================================================
END-TO-END TRIAGE REPORT
============================================================
Target folder: .../data/sample_evidence

Running processes (sample):
  {'pid': 1234, 'name': 'python'}

Recently modified files:
  notes.txt - 12s ago - 25 bytes

File hashes:
  notes.txt: <sha256>
  payload.bin: <sha256>
  report.txt: <sha256>

File timeline:
  ... | notes.txt | <hash>...
  ... | payload.bin | <hash>...
  ... | report.txt | <hash>...

============================================================
```

## Ethical / authorized use

This tool is intended for systems and files that you own or are explicitly
authorized to inspect. The sample data included in this repository is safe
local practice data. Do not use security or system-inspection tools against
third-party systems without authorization.

## Known limitations

- The file scan is limited to the target folder's immediate files; it does
  not recursively scan subdirectories.
- The recent-file check uses the local machine's current time.
- Process visibility depends on operating-system permissions.
- `psutil` is preferred; a read-only OS command is used as a fallback.
- SHA-256 is used for integrity identification, not as proof that a file is
  malicious or benign.
