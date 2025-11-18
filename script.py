import os

import pandas as pd
import requests
from dotenv import load_dotenv


def api_paginator(url, params, page_counter):
    response = requests.get(url, params)
    if response.status_code == 200:
        data = response.json()
        all_results = []

        while data['response']['pages'] > page_counter:
            page_counter += 1
            all_results.extend(data['response']['results'])

        dataset = pd.DataFrame(all_results)
        return dataset

    else:
        raise ValueError(f"Failed with status code: {response.status_code}")


load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")
page_counter = 1

params = {
    "q": "AI",
    "page": page_counter,
    "tag": "technology/google",
    "from-date": "2025-09-01",
    "api-key": API_KEY
}

dataframe = api_paginator(BASE_URL, params, page_counter)
print(dataframe)
