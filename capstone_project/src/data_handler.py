import requests
import json

response = requests.get("https://api.github.com/users/Narjes-almasri/repos")
if response.status_code == 200:
    convert_data = response.json()
    with open ("data.json","w") as f:
        json.dump(convert_data,f)
else:
    print("error :",response.status_code)
            
# print("Response:", response.json())
# print("status code",response.status_code)