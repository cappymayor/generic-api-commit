import json
import os

import requests

BASEURL = "https://content.guardianapis.com/search"


def guardian_api():
    api_key = os.getenv("GUARDIAN_API_KEY")
    if api_key is None:
        raise ValueError("ERROR: GUARDIAN_API_KEY is missing")

    params = {
        "api-key": api_key,
        "q": "fashion",
        "page-size": 50,
        "from-date": "2025-01-01",
        "to-date": "2025-01-30",
        "page": 1
    }

    response = requests.get(BASEURL, params=params)
    if response.status_code == 401:
        raise ValueError("Invalid API key")
    if response.status_code == 400:
        raise TypeError("invalid syntax")
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")

    first_page = response.json()
    total_pages = first_page["response"].get("pages", 1)
    print(f"Total pages available: {total_pages}")

    all_articles = []

    page = 1
    while page <= total_pages:
        print(f"Fetching page {page}...")

        params["page"] = page
        response = requests.get(BASEURL, params=params)

        data = response.json()
        results = data["response"]["results"]

        all_articles.extend(results)
        page += 1

    print(f"Finished! Total articles fetched: {len(all_articles)}")

    # Save JSON file
    with open("guardian_articles.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=4, ensure_ascii=False)

    print("Saved guardian_articles.json successfully.")


# Run the script
guardian_api()
