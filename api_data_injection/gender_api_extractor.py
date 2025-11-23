import pandas as pd
import requests

url = "https://randomuser.me/api/"
params = {
    'results': 100
    }
df = []


def gender_api():
    '''
    This functio extract female date from the API with age e
    equal to 40 ad above'''

    response = requests.get(url=url, params=params)
    results = response.json()['results']
    print(len(results))

    for article in results:
        gender = article['gender']
        age = article['dob']['age']
        if age >= 40 and gender == 'female':
            df.append(article)
    return df


data = pd.json_normalize(gender_api())
data.to_csv("data/new_gender.csv")

print(len(data))
