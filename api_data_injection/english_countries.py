import requests
import pandas as pd

url = "https://restcountries.com/v3.1/region/europe"


filtered_table = []

def countryFirstLaguage():
        '''
    The task to return European coutries that speak English
       '''


        response = requests.get(url)
        if response.status_code != 200:
            response.raise_for_status

        response = requests.get(url)

        unfiltered_data = response.json()

        for data in unfiltered_data:
            for i in data['languages'].values():
                if i == 'English':
                    eng_countries_filter={
                                          "country": data['name']['official'],
                                          "first_language": i
                                           }

                    filtered_table.append(eng_countries_filter)

        return filtered_table

eng_countries = pd.json_normalize(countryFirstLaguage())
print(f"Total Number of English Speaking Coutries in Europe: {len(eng_countries)}")

