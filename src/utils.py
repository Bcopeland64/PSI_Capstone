import csv
import os

def check_file_exists(file_path):
    # verifying file exists.
    if not os.path.exists(file_path):
        print("Error: The file does not exist ->", file_path)
        return False
    return True

def save_summary_to_csv(summary_data, output_path="triage_summary.csv"):
    # exporting summary to a csv file.
    try:
        f = open(output_path, "w", newline="", encoding="utf-8")
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key in summary_data:
            writer.writerow([key, summary_data[key]])
        f.close()
        print("\nResults saved to:", output_path)
    except Exception as e:
        print("Failed to write CSV:", e)