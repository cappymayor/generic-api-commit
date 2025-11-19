import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://content.guardianapis.com/search"
API_KEY = os.getenv("API_KEY")

params = {
    "q": "russian ukraine war"
}


try:
    response = requests.get(BASE_URL, params={**params, "api-key": API_KEY})
    if response.status_code != 200:
        print(f"Request failed. Status code {response.status_code}")
        raise Exception("API request failed")
except Exception as e:
    print(f"An error has occurred: {e}")
    raise

total_pages = response.json().get("response", {}).get("pages", 0)
all_articles = []


for page in range(1, total_pages + 1):
    try:
        response = requests.get(
            BASE_URL, params={**params, "api-key": API_KEY, "page": page})
        if response.status_code != 200:
            print(
                f"Page {page} failed. Status code {response.status_code}")
            break

        articles = response.json().get("response", {}).get("results", [])
        all_articles.extend(articles)
        print(f"Fetched page {page} of {total_pages}", end="\r")
    except Exception as e:
        print(f"An error occured on page {page}: {e}")
        break

articles_data = []
for article in all_articles:
    articles_data.append({
        "headline": article.get("webTitle", ""),
        "url": article.get("webUrl", ""),
        "date": article.get("webPublicationDate", "")
    })


articles = pd.DataFrame(articles_data)

print(articles)
