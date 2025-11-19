import os

import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

url = "https://content.guardianapis.com/search"
params = {
    "q": "Russia-Ukraine war",
    "from-date": "2024-01-01",
    "to-date": "2025-01-05",
    "api-key": os.getenv("GUARDIAN_API_KEY")
}

page = 1

# Store all results
all_results = []

while True:
    params["page"] = page
    response = requests.get(url, params=params)

    # Handle any status code that is not 200
    if response.status_code != 200:
        msg = (
            f"Request failed with status {response.status_code}: "
            f"{response.text}"
        )
        raise Exception(msg)

    data = response.json()

    # Collect data from this page
    results = data["response"]["results"]
    all_results.extend(results)

    # Stop AFTER processing if it's the last page
    if data["response"]["currentPage"] == data["response"]["pages"]:
        break

    page += 1

print(f"Total results fetched: {len(all_results)}")
