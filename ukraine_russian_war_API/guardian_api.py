
import json
import os

import requests

BASE_URL = "https://content.guardianapis.com/search"


def save_to_json(articles, filename="guardian_articles.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

    print(f"save_guardian_articles_to_json: {filename}")


def main():
    api_key = os.getenv("GUARDIAN_API_KEY")
    if api_key is None:
        raise ValueError("GUARDIAN_API_KEY is missing")

    params = {
        "api-key": api_key,
        "q": "Russia Ukraine war",
        "page-size": 50,
        "from-date": "2025-01-01",
        "to-date": "2025-01-30"
    }

    print("Sending first request to Guardian API...")

    params["page"] = 1
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 401:
        raise ValueError("Invalid API key")
    if response.status_code != 200:
        print("API returned an error:", response.status_code())
        raise Exception("Stopping execution due to API error.")
    data = response.json()
    total_pages = data["response"].get("pages", 1)
    print(f"Total pages available: {total_pages}")

    all_articles = []
    page = 1
    while page <= total_pages:
        print(f"Fetching page {page}...")
        params["page"] = page
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code()}")
            raise Exception("API error during pagination.")

        data = response.json()
        results = data["response"]["results"]
        all_articles.extend(results)
        page += 1

    print(f"Finished! Total articles fetched: {len(all_articles)}")

    save_to_json(all_articles, "guardian_articles.json")


if __name__ == "__main__":

    main()
