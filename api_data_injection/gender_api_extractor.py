import pandas as pd
import requests

url = "https://randomuser.me/api/"
params = {
    'results': 100
    }
filtered_data = []


def gender_api():
    '''
    The function returns female data from the API with age
    equal to 40 and above
    '''

    response = requests.get(url=url, params=params)
    if response.status_code != 200:
        response.raise_for_status()

    results = response.json()['results']
    print(f"Total Api records: {len(results)}") 


    for article in results:
        gender = article['gender']
        age = article['dob']['age']
        if age >= 40 and gender == 'female':
            filtered_data.append(article)
    return filtered_data


data = pd.json_normalize(gender_api())
data.to_csv("data/female_data.csv")

print(f"Total processed Record: {len(data)}")
