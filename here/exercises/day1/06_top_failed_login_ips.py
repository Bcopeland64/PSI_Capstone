# Ceiling: per-IP breakdown of failed logins, top 3
import re
from collections import Counter

counter = Counter()
with open("data/sample_auth.log") as f:
    for line in f:
        if "Failed password" in line:
            ip = re.search(r"\d+\.\d+\.\d+\.\d+",line)
            if ip:
                counter[ip.group()] +=1
print("top 3 ips :",counter.most_common(3))            