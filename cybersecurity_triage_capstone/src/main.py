"""Main entry point for the Cybersecurity Triage Tool."""

from models import TriageCase
from logic import calculate_risk, get_recommendation, search_cases
from data_handler import load_cases, save_cases
from utils import get_non_empty, get_integer, get_yes_no, print_case


def create_case(cases):
    """Collect user input, analyze it, and save a new triage case."""
    print("\n--- Create New Triage Case ---")

    case_id = get_non_empty("Case ID: ")
    if any(case.case_id == case_id for case in cases):
        print("A case with this ID already exists.")
        return

    case = TriageCase(
        case_id=case_id,
        file_name=get_non_empty("File name: "),
        file_size=get_integer("File size (bytes): "),
        executable=get_yes_no("Is the file executable? (yes/no): "),
        downloaded=get_yes_no("Was it downloaded from the Internet? (yes/no): "),
        antivirus_triggered=get_yes_no("Did antivirus trigger an alert? (yes/no): "),
        suspicious_extension=get_yes_no("Does it have a suspicious extension? (yes/no): "),
        notes=input("Notes (optional): ").strip(),
    )

    case.set_created_at()
    calculate_risk(case)
    cases.append(case)
    save_cases(cases)

    print("\nCase created successfully!")
    print_case(case)
    print(f"Recommendation: {get_recommendation(case.risk_level)}")


def view_cases(cases):
    """Display all saved cases."""
    if not cases:
        print("\nNo cases found.")
        return

    print(f"\nTotal cases: {len(cases)}")
    for case in cases:
        print_case(case)


def search_saved_cases(cases):
    """Search saved cases using a keyword."""
    keyword = get_non_empty("Search keyword: ")
    results = search_cases(cases, keyword)

    if not results:
        print("No matching cases found.")
        return

    print(f"\nFound {len(results)} case(s):")
    for case in results:
        print_case(case)


def generate_report(cases):
    """Print a simple summary report."""
    print("\n--- Triage Summary Report ---")
    if not cases:
        print("No cases available.")
        return

    high = sum(case.risk_level == "HIGH" for case in cases)
    medium = sum(case.risk_level == "MEDIUM" for case in cases)
    low = sum(case.risk_level == "LOW" for case in cases)

    average = sum(case.risk_score for case in cases) / len(cases)

    print(f"Total cases: {len(cases)}")
    print(f"High risk:   {high}")
    print(f"Medium risk: {medium}")
    print(f"Low risk:    {low}")
    print(f"Average risk score: {average:.2f}/10")


def main():
    """Run the interactive CLI application."""
    cases = load_cases()

    while True:
        print("\n" + "=" * 45)
        print("      CYBERSECURITY TRIAGE TOOL")
        print("=" * 45)
        print("1. Create new case")
        print("2. View all cases")
        print("3. Search cases")
        print("4. Generate summary report")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_case(cases)
        elif choice == "2":
            view_cases(cases)
        elif choice == "3":
            search_saved_cases(cases)
        elif choice == "4":
            generate_report(cases)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
