
import json
import os

import requests


def save_to_json(articles, filename="guardian_articles.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

    print(f"Saved JSON file: {filename}")


def main():
    api_key = os.getenv("GUARDIAN_API_KEY")

    if not api_key:
        raise ValueError("ERROR: GUARDIAN_API_KEY not set.")

    end_point_url = "https://content.guardianapis.com/search"

    params = {
        "api-key": api_key,
        "q": "Russia Ukraine war",
        "page-size": 50,
        "from-date": "2024-01-01",
        "to-date": "2025-01-30",
        "page": 1
    }

    print("Sending first request to Guardian API...")

    response = requests.get(end_point_url, params=params)
    if response.status_code != 200:
        print("API returned an error:", response.status_code)
        raise Exception("Stopping execution due to API error.")

    try:
        data = response.json()
    except Exception:
        raise ValueError("Response is not valid JSON.")
    if "response" not in data or "pages" not in data["response"]:
        raise KeyError("Missing 'response' or 'pages' in API data.")

    total_pages = data["response"]["pages"]
    print(f"Total pages available: {total_pages}")
    all_articles = []
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page} of {total_pages}...")

        params["page"] = page

        response = requests.get(end_point_url, params=params)

        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            raise Exception("API error during pagination.")

        try:
            data = response.json()
        except Exception:
            raise ValueError(f"Page {page}: Failed to decode JSON.")

        if "response" not in data or "results" not in data["response"]:
            raise KeyError(f"Page {page}: Unexpected response structure.")

        results = data["response"]["results"]
        all_articles.extend(results)

    print(f"Finished! Total articles fetched: {len(all_articles)}")

    save_to_json(all_articles, "guardian_articles.json")


if __name__ == "__main__":

    main()
