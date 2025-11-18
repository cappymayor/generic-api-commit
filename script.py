import os

import pandas as pd
import requests
from dotenv import load_dotenv


def api_paginator(url, params):
    response = requests.get(url, params)

    if response.status_code == 200:
        data = response.json()
        all_results = []

        while params["page"] <= data['response']['pages']:
            next_page = requests.get(url, params)
            more_news = next_page.json()

            all_results.extend(more_news['response']['results'])
            params["page"] += 1

        dataset = pd.DataFrame(all_results)
        return dataset

    else:
        response.raise_for_status()


load_dotenv()
BASE_URL = os.environ.get("BASE_URL")

params = {
    "q": "AI",
    "page": 1,
    "tag": "technology/google",
    "from-date": "2025-09-01",
    "api-key": os.environ.get("API_KEY")
}

dataframe = api_paginator(BASE_URL, params)
print(dataframe)
