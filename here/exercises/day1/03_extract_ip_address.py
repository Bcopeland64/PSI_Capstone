# regular expression module for pattern matching
# Technique 3: extract a pattern (an IP address) with re.search()

########### notes about re.search() :
# it return object of Matched thing that containes info like where it found what it found and so on 
# so we use .group() in order to just get the thing we are searching for without th extra info

import re
line = "2026-02-10 08:04:59 WARNING Connection retry to 172.16.0.7" 

ip = re.search(r"\d+\.\d+\.\d+\.\d+",line)

if ip:
    final_ip=ip.group()
    print(final_ip)
else:
  print(None)      

# print(ip) => $  py ex3.py  <re.Match object; span=(48, 58), match='172.16.0.9'> it will give us the whole object with the extra info like  where it found what it found 