import csv

import requests

API_KEY = " e58deace-2a4d-4355-8b07-f225eaf5b467"
BASE_URL = "https://content.guardianapis.com/search"


def fetch_all_articles(query, max_pages=2):
    """Fetch all articles for a given query from the Guardian API."""
    page = 1
    all_results = []

    while True:
        try:
            params = {
                "q": query,
                "api-key":  "e58deace-2a4d-4355-8b07-f225eaf5b467",
                "page": page,
                "page-size": 50,
                "show-fields": "headline,bodyText"
            }

            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = data["response"]["results"]
            all_results.extend(results)

            print(f"Fetched page {page}")

            if page >= data["response"]["pages"] or page >= max_pages:
                break

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            break

    return all_results


# Fetch articles
articles = fetch_all_articles("Russia Ukraine war", max_pages=2)
print(f"Total articles fetched: {len(articles)}")


# Save to CSV
with open("guardian_articles.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["id", "webTitle", "webUrl", "headline", "bodyText"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for article in articles:
        writer.writerow({
            "id": article.get("id"),
            "webTitle": article.get("webTitle"),
            "webUrl": article.get("webUrl"),
            "headline": article.get("fields", {}).get("headline"),
            "bodyText": article.get("fields", {}).get("bodyText")
        })