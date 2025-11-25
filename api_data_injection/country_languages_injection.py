import pandas as pd
import requests

url = "https://restcountries.com/v3.1/region/europe"
targeted_data = []


def country_lang():
    '''
    The function is task to filter and return official countries 
    name and there languages from the api unfiltered data
    '''


    response = requests.get(url)
    if response.status_code != 200:
        response.raise_for_status

    unfiltered_data = response.json()
    print(f"Numbers of unfiltered data: {len(unfiltered_data)}")

    for data in unfiltered_data:
        if len(data['languages']) > 2:
            country = data['name']['official']
            languages = data['languages']
            languages_values = ', '.join(languages.values())
            targeted_data.append({
                    "country": country,
                    "languages": languages_values})
    return targeted_data

country_languages = pd.DataFrame(country_lang())
print(f"Total Number of Filtered Data : {len(country_languages)}")
