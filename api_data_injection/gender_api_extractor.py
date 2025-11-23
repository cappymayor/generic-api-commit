import pandas as pd
import requests

url = "https://randomuser.me/api/"
params = {
    'results': 100
    }
df = []


def gender_api():
    '''
    This functio extract female data from the API with age
    equal to 40 ad above'''

    response = requests.get(url=url, params=params)
    if response.status_code != 200:
        print(response.raise_for_status())
    else:
        results = response.json()['results']
        print(len(results))

    for article in results:
        gender = article['gender']
        age = article['dob']['age']
        if age >= 40 and gender == 'female':
            df.append(article)
    return df


data = pd.json_normalize(gender_api())
data.to_csv("data/female_data.csv")

print(len(data))
