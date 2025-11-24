import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("BASE_URL")

params = {
    "q": "AI",
    "page": 1,
    "tag": "technology/google",
    "from-date": "2025-09-01",
    "api-key": os.environ.get("API_KEY")
}

total_pages = 1


def api_paginator(url, params, total_pages):
    all_results = []

    while params["page"] <= total_pages:
        response = requests.get(url, params)

        if response.status_code == 200:
            news = response.json()
            total_pages = news['response']['pages']

            all_results.extend(news['response']['results'])
            params["page"] += 1

        else:
            response.raise_for_status()

    dataset = pd.json_normalize(all_results)
    return dataset


dataframe = api_paginator(url, params, total_pages)
print(dataframe)
