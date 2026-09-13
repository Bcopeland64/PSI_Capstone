#we have a line we wanna split it into fields

line = "2026-02-10 08:02:15 WARNING Connection retry to 172.16.0.4"  

Date , Time , Status , *remaining , ip = line.split()

print("Date   : ",Date)
print("Time   : ",Time)
print("Status : ",Status)
print("IP     : ",ip)
print("remainig :", remaining)

#the output is:
# $ py ex2.py 
# Date   :  2026-02-10
# Time   :  08:02:15
# Status :  WARNING
# IP     :  172.16.0.4
# remainig : ['Connection', 'retry', 'to'] to make this looks as one sentence we have to use join

msg = " ".join(remaining)
print("msg after join :", msg) #msg after join : Connection retry to
