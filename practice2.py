import requests
import csv

API_KEY = "e58deace-2a4d-4355-8b07-f225eaf5b467"  # define your key securely
URL = "https://content.guardianapis.com/search"


def fetch_articles(query):
    """Fetch articles from the Guardian API matching the query."""
    page = 1
    all_data = []  # list to store results

    while True:
        params = {
            "q": query,
            "api-key": API_KEY,
            "page": page,
            "page-size": 50,  # 50 results per page
            "show-fields": "headline,bodyText",
        }

        response = requests.get(URL, params=params, timeout=10)

        if response.status_code != 200:
            # Handle non-200 responses
            print(f"Error: Received status code {response.status_code}")
            break  # stop fetching further pages

        data = response.json()
        results = data["response"]["results"]
        all_data.extend(results)  # add results as single iterable

        if page >= data["response"]["pages"]:
            break

        page += 1

    return all_data


def save_articles_to_csv(articles, filename="guardian.csv"):
    """Save articles to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Headline", "Body"])

        for article in articles:
            headline = article.get("fields", {}).get("headline", "")
            body = article.get("fields", {}).get("bodyText", "")
            writer.writerow([headline, body])


if __name__ == "__main__":
    articles = fetch_articles("Russia Ukraine war")
    if articles:
        save_articles_to_csv(articles)
        print(f"Saved {len(articles)} articles to CSV.")
    else:
        print("No articles fetched.")
