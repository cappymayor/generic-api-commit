import os

import requests


def fetch_articles(query):
    """
    Fetch articles from The Guardian API using pagination.
    Args:
        query (str): The search term for articles.

    Returns:
        list: A list of article dictionaries.
    """
    # Get API key from environment variables
    api_key = os.getenv("GUARDIAN_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing GUARDIAN_API_KEY. Set it in your environment variables."
        )

    page = 1
    all_articles = []

    while True:
        url = "https://content.guardianapis.com/search"
        params = {
            "q": query,
            "api-key": api_key,
            "page-size": 50,
            "page": page
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as error:
            print(f"Error fetching page {page}: {error}")
            break

        results = data["response"]["results"]
        all_articles.extend(results)

        current_page = data["response"]["currentPage"]
        total_pages = data["response"]["pages"]

        print(f"Fetched page {current_page}/{total_pages}")

        if current_page >= total_pages:
            break

        page += 1

    return all_articles
