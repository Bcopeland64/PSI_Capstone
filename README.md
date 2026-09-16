# Password Vault & Strength Analyzer — Cyber Security CLI Tool

A capstone project for the Python Workshop. An interactive
command-line application that securely stores credentials
(encrypted at rest with AES via `cryptography.Fernet`), analyzes
password strength, detects password reuse across services, and
generates strong random passwords.

## Security Design

- **Nothing is ever stored in plaintext.** Every password is
  encrypted with a key derived from your master password using
  PBKDF2-HMAC-SHA256 (390,000 iterations) before being written to
  SQLite.
- **The master password itself is never stored.** Only a random
  salt and an encrypted "verifier" string are kept, used solely to
  confirm the correct master password was entered on unlock.
- **Reports never leak passwords.** The vault health report and CSV
  export only ever include service names, usernames, and strength
  ratings — never the passwords themselves.
- This is a defensive security tool (a password manager), not an
  offensive one — it does not attempt to crack, guess, or exfiltrate
  anyone else's credentials.

## Features

- Add credentials (service, username, password) with immediate
  strength feedback.
- List all credentials in a formatted table (via `rich`), passwords
  revealed only after unlocking the vault with the master password.
- Look up credentials by service name.
- Vault health report: average strength score, weak-password count,
  and reused-password warnings.
- Generate cryptographically random strong passwords.
- Export a security summary to CSV (metadata only, no passwords).
- Delete a credential by ID.

## Project Structure

```
security_vault/
├── data/
│   ├── sample_data.csv     # Illustrative example (no real secrets)
│   └── vault.db             # Created automatically on first run
├── src/
│   ├── __init__.py
│   ├── main.py               # CLI entry point / menu loop
│   ├── models.py             # Credential dataclass
│   ├── security.py            # Encryption, key derivation, strength analysis
│   ├── data_handler.py        # SQLite persistence layer
│   └── utils.py                # Input validation
├── tests/
│   └── test_logic.py           # Pytest unit tests
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
# 1. Clone your fork
git clone <your-fork-url>
cd security_vault

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the App

From the project root:

```bash
python -m src.main
```

On first run you'll be asked to choose a master password (this
initializes your vault). On future runs you'll be asked to enter it
to unlock the vault. **There is no password reset** — if you forget
your master password, the encrypted data cannot be recovered. This
is by design (the same trade-off real password managers make).

```
========== Password Vault ==========
1. Add credential
2. List all credentials (reveal passwords)
3. Look up by service
4. Vault health report
5. Generate a strong password
6. Export security summary to CSV (no passwords included)
7. Delete a credential
8. Exit
======================================
```

## Running Tests

```bash
pytest
```

## Design Notes

- **Modular architecture**: encryption/analysis (`security.py`),
  persistence (`data_handler.py`), data model (`models.py`),
  validation (`utils.py`), reporting (`logic.py`), and the CLI
  (`main.py`) are all separated so each piece can be tested and
  changed independently.
- **OOP**: `Credential` is a `dataclass`; `VaultDatabase` encapsulates
  all SQLite access behind a small, well-defined interface.
- **Data persistence**: encrypted credentials are stored in a local
  SQLite database (`data/vault.db`), created automatically on first
  run.
- **Error handling**: all user input is validated (`utils.py`), and
  every database, encryption, and file operation is wrapped in
  `try/except` with clear, actionable error messages.
- **Third-party packages**: `cryptography` for AES encryption and
  key derivation, `rich` for formatted terminal tables, `pytest` for
  the test suite.

## Possible Extensions

- Add a password-expiry reminder (flag credentials older than N days).
- Support exporting/importing an encrypted backup of the whole vault.
- Add a check against a local list of known-breached passwords
  (e.g. a downloaded Have I Been Pwned hash range) for extra credit.
