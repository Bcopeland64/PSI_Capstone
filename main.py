

"""Main entry point for running the Triage CLI Tool."""

import sys
from logic import TriageScanner
from utils import file_exists, validate_host


def main():
  print("=" * 50)
  print("   Automated Incident Triage System (CLI)")
  print("=" * 50)

  target_host = "127.0.0.1"
  if not validate_host(target_host):
    print("[-] Invalid host configuration.")
    sys.exit(1)

  scanner = TriageScanner(target_host=target_host)

  # 1. Network Audit
  ports = [22, 80, 443, 8080]
  print(f"\n[+] Auditing Ports on {target_host}:")
  port_results = {}
  for port in ports:
    is_open = scanner.check_port(port)
    port_results[str(port)] = "OPEN" if is_open else "CLOSED"
    print(f"  - Port {port}: {port_results[str(port)]}")

  # 2. File Audit
  target_file = "src/main.py"
  print(f"\n[+] Inspecting Artifact: {target_file}")
  try:
    if file_exists(target_file):
      file_meta = scanner.audit_file(target_file)
      print(f"  - Size: {file_meta['size_bytes']} Bytes")
      print(f"  - Modified: {file_meta['last_modified']}")
      print(f"  - SHA256: {file_meta['sha256_hash']}")

      # 3. Save JSON Report
      report_data = {
          "host_audit": port_results,
          "file_artifact": file_meta,
      }
      report_path = "data/triage_report.json"
      scanner.save_report(report_data, report_path)
      print(f"\n[+] Report saved successfully to {report_path}")
  except Exception as e:
    print(f"[-] Error during execution: {e}")


if __name__ == "__main__":
  main()