import re

def find_matching_lines(filename, keyword):
    matches = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if keyword in line:
                matches.append(line)

    return matches


results = find_matching_lines("auth.log", "Failed")

print("Failed login attempts:", len(results))

ip_counts = {}

for line in results:
    match = re.search(r"\d+\.\d+\.\d+\.\d+", line)

    if match:
        ip = match.group()

        if ip in ip_counts:
            ip_counts[ip] += 1
        else:
            ip_counts[ip] = 1

print("Source IP counts:")

for ip, count in ip_counts.items():

    if ip.startswith(("10.", "172.16.", "192.168.")):
        ip_type = "Private"
    else:
        ip_type = "Public"

    print(ip, "->", count, "-", ip_type)