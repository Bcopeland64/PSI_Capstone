
data = """ 2026-02-10 08:01:00 INFO  Service started
2026-02-10 08:02:15 WARNING Connection retry to 172.16.0.4
2026-02-10 08:03:40 INFO  Health check OK
2026-02-10 08:04:59 WARNING Connection retry to 172.16.0.9
 """

    # f.write(data)
with open("data/demo_service.log", "r") as f:
    # We open the file "data.log" in read mode ("r")
    # and give the opened file the name/alias "f".

    for line in f:
        # We go through the file one line at a time
        # and store the current line in the variable "line".

        if "INFO" in line:
            # We check whether the current line contains the word "INFO".

            print(line.strip())
            # We print the line after removing whitespace/newline characters
            # from the beginning and end of the line. 

            
################## the output with strip() vs  without ######################
#  if we use print(line) without strip() it will print the output like this with newline           
# narjes@DESKTOP-LVUHLVL MINGW64 C:/Users/narjes/Desktop/py/mytests/day1.py (day1-practice)
# $ py d1.py 
# 2026-02-10 08:01:00 INFO  Service started
# \n
# 2026-02-10 08:03:40 INFO  Health check OK
######################################## 
# but with strip print(line.strip()) the output is like:
# narjes@DESKTOP-LVUHLVL MINGW64 C:/Users/narjes/Desktop/py/mytests/day1.py (day1-practice)
# $ py d1.py 
# 2026-02-10 08:01:00 INFO  Service started
# 2026-02-10 08:03:40 INFO  Health check OK
