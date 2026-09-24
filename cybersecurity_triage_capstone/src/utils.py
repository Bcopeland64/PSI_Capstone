"""Input validation and display helpers."""


def get_non_empty(prompt):
    """Read a required non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def get_integer(prompt, minimum=0):
    """Read an integer greater than or equal to minimum."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value < minimum:
                print(f"Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid number. Please try again.")


def get_yes_no(prompt):
    """Read a yes/no answer and return a Boolean."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("yes", "y"):
            return True
        if value in ("no", "n"):
            return False
        print("Please enter yes or no.")


def print_case(case):
    """Display a single triage case."""
    print("\n" + "=" * 45)
    print(f"Case ID:              {case.case_id}")
    print(f"File:                 {case.file_name}")
    print(f"File size:            {case.file_size} bytes")
    print(f"Executable:           {'Yes' if case.executable else 'No'}")
    print(f"Downloaded:           {'Yes' if case.downloaded else 'No'}")
    print(f"Antivirus triggered:  {'Yes' if case.antivirus_triggered else 'No'}")
    print(f"Suspicious extension: {'Yes' if case.suspicious_extension else 'No'}")
    print(f"Risk score:           {case.risk_score}/10")
    print(f"Risk level:           {case.risk_level}")
    print(f"Notes:                {case.notes}")
    print(f"Created:              {case.created_at}")
    print("=" * 45)
