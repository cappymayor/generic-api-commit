import requests
import csv

API_KEY = "e58deace-2a4d-4355-8b07-f225eaf5b467"
BASE_URL = "https://content.guardianapis.com/search"

def fetch_all_articles(query):
    page = 1
    all_results = []

    while True:
        try:
            params = {
                "q": query,
                "api-key": API_KEY,
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

            if page >= data["response"]["pages"]:
                break
            
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            break

    return all_results

# Fetch articles on Russia–Ukraine war
articles = fetch_all_articles("Russia Ukraine war")
print(f"Total articles fetched: {len(articles)}")

# Save articles to CSV
csv_file = "russia_ukraine_articles.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Headline", "Body"])  # CSV header

    for article in articles:
        headline = article["fields"].get("headline", "")
        body = article["fields"].get("bodyText", "")
        writer.writerow([headline, body])

print(f"Articles saved to {csv_file}")