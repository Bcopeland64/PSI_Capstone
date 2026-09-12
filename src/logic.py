import csv
import hashlib
import os
import subprocess
from collections import Counter

# main class that handles security triage and log analysis.
class SecurityTriage:
    def __init__(self, data_file):
        self.data_file = data_file

    def get_sample_processes(self):
        procs = []
        try:
            import psutil
            for p in psutil.process_iter(["pid", "name"]):
                procs.append(p.info["name"])
                if len(procs) == 5:
                    break
            return procs
        except ImportError:
            res = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            lines = res.stdout.splitlines()
            return lines[:5]

    #calculating hash for dataset.
    def hash_data_file(self):
        f = open(self.data_file, "rb")
        content = f.read()
        f.close()
        return hashlib.sha256(content).hexdigest()

    def analyze_traffic_csv(self):
        suspicious_ports = ["4444", "31337"]
        port_list = []
        suspicious_hits = 0

        f = open(self.data_file, "r", encoding="utf-8")
        reader = csv.DictReader(f)
        for row in reader:
            port = row["dst_port"]
            port_list.append(port)
            if port in suspicious_ports:
                suspicious_hits = suspicious_hits + 1
        f.close()

        port_counter = Counter(port_list)
        return {
            "top_ports": port_counter.most_common(2),
            "suspicious_events": suspicious_hits
        }