import sys
from src.logic import NetLogSecAnalyzer

def print_menu():
    print("\n=============================================")
    print("        NetLogSec - Security Analyzer        ")
    print("=============================================")
    print("1. Load and Parse Log File")
    print("2. Detect Brute Force Attacks (Time-Window)")
    print("3. Export Comprehensive Log Report (CSV)")
    print("4. Exit")

def main():
    analyzer = None
    
    while True:
        print_menu()
        choice = input("Select an option (1-4): ").strip()
        
        try:
            if choice == "1":
                file_path = input("Enter log file path (e.g., data/sample_auth.log): ").strip()
                analyzer = NetLogSecAnalyzer(file_path)
                analyzer.parse_logs()
                print(f"[+] Successfully loaded and parsed logs!")
                
            elif choice == "2":
                if not analyzer:
                    print("[-] Warning: Please load a log file first (Option 1).")
                    continue
                
                minutes = int(input("Enter time window in minutes (default 5): ") or 5)
                threshold = int(input("Enter failed attempts threshold (default 3): ") or 3)
                
                alerts = analyzer.detect_brute_force(time_window_minutes=minutes, threshold=threshold)
                
                print("\n--- Brute Force Detection Results ---")
                if not alerts:
                    print("No suspicious brute-force activity detected.")
                else:
                    for alert in alerts:
                        print(alert)
                        
            elif choice == "3":
                if not analyzer:
                    print("[-] Warning: Please load a log file first.")
                    continue
                out_path = input("Enter output CSV report path (e.g., data/report.csv): ").strip()
                analyzer.export_comprehensive_report(out_path)
                print(f"[+] Report exported successfully to: {out_path}")
                
            elif choice == "4":
                print("Exiting NetLogSec. Stay secure!")
                sys.exit(0)
            else:
                print("[-] Invalid option. Please choose a number between 1 and 4.")
                
        except FileNotFoundError as e:
            print(f"[-] File Error: {e}")
        except ValueError:
            print("[-] Input Error: Please enter valid numbers where required.")
        except Exception as e:
            print(f"[-] Unexpected Error: {e}")

if __name__ == "__main__":
    main()