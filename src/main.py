import sys
from utils import hash_file, scan_port, fetch_api_data
from logic import parse_connections, find_top_talker, save_triage_report
def main():
    while True:
        print("\n=== Security Triage Tool ===")
        print("1. Hash a File")
        print("2. Scan a Port")
        print("3. Analyze Traffic & Generate Report")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            filepath = input("Enter path to file: ").strip()
            result = hash_file(filepath)
            print(f"Hash Result: {result}")

        elif choice == "2":
            host = input("Enter host or IP: ").strip()
            port_input = input("Enter port number: ").strip()
            try:
                port = int(port_input)
                is_open = scan_port(host, port)
                status = "OPEN" if is_open else "CLOSED"
                print(f"Port {port} on {host} is: {status}")
            except ValueError:
                print("Invalid port number.")

        elif choice == "3":
            csv_path = input("Enter CSV path (e.g. data/sample_data.csv): ").strip()
            traffic = parse_connections(csv_path)
            if traffic:
                top_ip, total_bytes = find_top_talker(traffic)
                print(f"[+] Top Talker: {top_ip} with {total_bytes} bytes")
                
                report = [
                    "=== Triage Report ===",
                    f"Top Talker IP: {top_ip}",
                    f"Total Bytes Sent: {total_bytes}"
                ]
                save_triage_report(report, "data/report.txt")

        elif choice == "4":
            print("Exiting tool. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()