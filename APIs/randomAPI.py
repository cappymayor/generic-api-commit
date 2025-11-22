import pandas as pd
import requests

""" The fetching part """
url = "https://randomuser.me/api/?results=100"

response = requests.get(url)
# print(response)
response = response.json()
response.keys()

results = response["results"]
# print(results)

"""The conditional statement part for filtering"""

Young_females = []
for i in results:
    if i["gender"] == "female" and i["dob"]["age"] < 43:
        Young_females.append(i)
print(Young_females)


df = pd.DataFrame(Young_females)
print(df)

print(f"There are {len(df)} females aged below 43 years in the list.")
