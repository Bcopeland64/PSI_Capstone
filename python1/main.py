from logic import TriageTool
from utils import check_file_exists, clean_input

def show_menu():
    print("\n--- Security Incident Triage CLI ---")
    print("1. Load Incident File")
    print("2. Show All Incidents")
    print("3. Filter Incidents by Severity")
    print("4. Export Summary Report")
    print("5. Exit")

def main():
    tool = TriageTool()

    while True:
        show_menu()
        choice = clean_input(input("Choose an option (1-5): "))

        if choice == "1":
            file_path = clean_input(input("Enter file path (e.g., data/sample_data.csv): "))
            if check_file_exists(file_path):
                if tool.load_data(file_path):
                    print("Data loaded successfully!")
            else:
                print("File not found. Please check the path and try again.")

        elif choice == "2":
            if tool.df is not None:
                print("\n--- Loaded Incidents ---")
                print(tool.df)
            else:
                print("Please load a file first (Option 1).")

        elif choice == "3":
            if tool.df is not None:
                sev = clean_input(input("Enter severity (LOW, MEDIUM, HIGH, CRITICAL): "))
                results = tool.filter_severity(sev)
                if results is not None and not results.empty:
                    print(f"\n--- {sev.upper()} Severity Incidents ---")
                    print(results)
                else:
                    print("No matching logs found for that severity.")
            else:
                print("Please load a file first (Option 1).")

        elif choice == "4":
            if tool.df is not None:
                out_path = clean_input(input("Enter export filename (e.g., report.json): "))
                tool.export_summary(out_path)
            else:
                print("Please load a file first (Option 1).")

        elif choice == "5":
            print("Exiting Triage Tool. Goodbye!")
            break

        else:
            print("Invalid selection. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()