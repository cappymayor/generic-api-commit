import pandas as pd
import requests

url = "https://randomuser.me/api/"
params = {
    'gender': 'female',
    'results': 100
    }

response = requests.get(url=url, params=params)
response.json()

new_data = response.json()
keys = new_data.keys()
infor = new_data['info']
results = new_data['results']
total_results = len(results)
print(total_results)

def gender_api():
    df = []
    for i in results:
        if 'dob' in i:
            if i['dob']['age'] >= 40:
                df.append(i)
    return df


data = pd.json_normalize(gender_api())
data.to_csv("data/new_gender.csv")

print(len(data))
