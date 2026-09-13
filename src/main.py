from data_handler import read_log_file, save_results
from logic import LogAnalyzer
from utils import validate_file_path, check_connection


def main():
    """Run the Security Log Analyzer application."""
    print("=== Security Log Analyzer ===")
if check_connection():
    print("Internet connection: OK")
else:
    print("Internet connection: unavailable")    

    try:
        file_path = input("Enter the log file path: ")
        file_path = validate_file_path(file_path)

        log_lines = read_log_file(file_path)

        analyzer = LogAnalyzer(log_lines)
        counts = analyzer.count_levels()

        print("\nLog Analysis Results:")
        print(f"INFO: {counts['INFO']}")
        print(f"WARNING: {counts['WARNING']}")
        print(f"ERROR: {counts['ERROR']}")

        save_results(counts, "data/analysis_results.txt")
        print("\nResults saved to data/analysis_results.txt")

    except (ValueError, FileNotFoundError, OSError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()