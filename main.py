import json

from utils.fetch_guardian import fetch_articles


def save_to_json(data, filename="results.json"):
    """Save extracted articles into a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Saved {len(data)} articles to {filename}")


if __name__ == "__main__":
    query = "russia ukraine war"
    articles = fetch_articles(query)
    save_to_json(articles)
