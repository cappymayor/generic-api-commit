import logging
import os

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

api_key = os.getenv("GUARDIAN_API_KEY")

base_url = "https://content.guardianapis.com/search"

query_container = []

parameters = {
    "api-key": api_key,
    "q": "ukraine-Russian-war",
    "page-size": 20,
    "order-by": "newest",
    "from-date": "2025-11-15",
    "to-date": "2025-11-24",
}


def guardian_api_content():
    """
    Fetch paginated articles from the Guardian API.

    This function sends repeated GET requests to the Guardian Content API,
    handling pagination automatically. Each page of results is appended
    to the global QUERY_CONTAINER list. The function uses the PARAMETERS
    dictionary for query configuration and logs each page fetched.
    """
    current_page = 1
    total_pages = 1

    while current_page <= total_pages:
        response = requests.get(base_url, params=parameters)

        if response.status_code != 200:
            response.raise_for_status()

        data = response.json()

        for article in data["response"]["results"]:
            query_container.append(article)

        logging.info(f"Fetched page {current_page}/ {total_pages}")

        total_pages = data["response"]["pages"]
        current_page += 1


def main():
    guardian_api_content()
    df = pd.json_normalize(query_container)
    print(df)
    print(f"Total articles fetched: {len(query_container)}")


if __name__ == "__main__":
    main()
