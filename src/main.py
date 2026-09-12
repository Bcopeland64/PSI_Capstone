import sys
from logic import SecurityTriage
from utils import check_file_exists, save_summary_to_csv

def main():
    
    target_csv = "data/sample_data.csv"
    if len(sys.argv) > 1:
        target_csv = sys.argv[1]

    print("--- Starting Triage Script ---")
    print("Checking file:", target_csv)

    if not check_file_exists(target_csv):
        return

    triage = SecurityTriage(target_csv)

    # 1) running process check
    print("\n[*] Sampling running processes:")
    processes = triage.get_sample_processes()
    for proc in processes:
        print("   -", proc)

    # 2) Hashing the data file
    file_hash = triage.hash_data_file()
    print("\n[*] Target File SHA-256:", file_hash[:16], "...")

    # 3. Analyzing network logs
    print("\n[*] Analyzing traffic log...")
    results = triage.analyze_traffic_csv()
    print("   - Top Destination Ports:", results["top_ports"])
    print("   - Suspicious Flagged Events:", results["suspicious_events"])

    # 4. Save results to csv
    summary_data = {
        "target_file": target_csv,
        "sha256_short": file_hash[:16],
        "top_ports": str(results["top_ports"]),
        "suspicious_count": results["suspicious_events"]
    }
    save_summary_to_csv(summary_data)
    print("\n[+] Triage completed successfully.")

if __name__ == "__main__":
    main()