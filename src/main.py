import csv
import hashlib
import os
import socket
from collections import Counter
import requests


# --- Ex 1: API Request ---
def fetch_uuid():
    """Fetch a random UUID from external API."""
    print("\n--- 1. Fetching UUID from API ---")
    try:
        r = requests.get("https://httpbin.org/uuid", timeout=5)
        r.raise_for_status()
        uuid_val = r.json().get("uuid")
        print(f"[+] UUID Received: {uuid_val}")
        return uuid_val
    except Exception as e:
        print(f"[!] API Request failed: {e}")
        return None


# --- Ex 2: CSV Traffic Analysis ---
def analyze_traffic(csv_path):
    """Generate sample network traffic data and analyze top talker IP."""
    print("\n--- 2. Analyzing Network Traffic ---")

    csv_data = """timestamp,src_ip,dst_port,protocol,bytes
2026-03-02T11:00:01,10.2.0.5,443,tcp,4000
2026-03-02T11:00:04,10.2.0.6,53,udp,120
2026-03-02T11:00:09,10.2.0.5,443,tcp,6500
2026-03-02T11:00:15,10.2.0.7,8080,tcp,300
2026-03-02T11:00:22,10.2.0.6,53,udp,90
2026-03-02T11:00:30,10.2.0.5,443,tcp,2200"""


    with open(csv_path, "w") as f:
        f.write(csv_data)

    ip_bytes = Counter()
    with open(csv_path, "r") as f:
        for row in csv.DictReader(f):
            ip_bytes[row["src_ip"]] += int(row["bytes"])

    top_talker, total = ip_bytes.most_common(1)[0]
    print(f"[+] Top talker: {top_talker} ({total} bytes)")


# --- Ex 3: File Hashing & Port Scanning ---
def quick_check(path, host, port):
    """Calculate SHA256 of a file and check socket connection on target port."""
    print("\n--- 3. Artifact Integrity & Port Check ---")

    # 1. Calculate SHA256
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("test content\n")

    with open(path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    # 2. Check Port Status
    s = socket.socket()
    s.settimeout(2)
    status = "open" if s.connect_ex((host, int(port))) == 0 else "closed"
    s.close()

    result = {"sha256": file_hash, "port_status": status}
    print(
        f"[+] SHA256 Hash: {result['sha256']}\n[+] Port {port} Status: {result['port_status']}"
    )
    return result


if __name__ == "__main__":
    print("==========================================")
    print(" 🚀 Python for Security - Capstone Engine ")
    print("==========================================")

    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    csv_file = os.path.join(data_dir, "exercise_connections.csv")
    sample_file = os.path.join(data_dir, "sample_file.txt")


    fetch_uuid()
    analyze_traffic(csv_file)
    quick_check(sample_file, "127.0.0.1", 22)

    print("\n[+] All tasks completed successfully!")