# Floor: total failed-login count using simple count sum()

# with open("sample_auth.log") as f:
#     for line in f:
#         if "Failed password" in line:
#             count = sum(1) this incorrect cuz sum needs smth iteratable inside it 
            
#     print("total Failed password = ",count)


# Floor: total failed-login count using simple count sum()

with open("data/sample_auth.log") as f:
   
    count = sum(1 for line in f if "Failed password" in line)
            
    print("total Failed password = ",count)