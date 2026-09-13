import csv
from collections import Counter
def parse_connections(csv_path):
    traffic_counter = Counter()
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip = row["src_ip"]
                bytes_count = int(row["bytes"])
                traffic_counter[ip] += bytes_count
        return traffic_counter
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return None
    except Exception as e:
        print(f"Error parsing connections: {e}")
        return None
def find_top_talker(traffic_counter):
    if not traffic_counter:
        return None, 0
    top_ip, total_bytes = traffic_counter.most_common(1)[0]
    return top_ip, total_bytes
def save_triage_report(report_lines, output_file="report.txt"):
    try:
        with open(output_file, mode="w", encoding="utf-8") as f:
            for line in report_lines:
                f.write(line + "\n")
        print(f"[+] Report saved successfully to: {output_file}")
        return True
    except Exception as e:
        print(f"[-] Failed to save report: {e}")
        return False