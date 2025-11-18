import requests
from dotenv import load_dotenv
import os

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

while True:
    params["page"] = page
    response = requests.get(url, params=params)
    data = response.json()

    # Check if the endpoint or response format changed
    if "response" not in data:
        print("API response format changed. Cannot find expected data.")
        break

    # Process the data on this page
    print("Page {page} results:")
    print(data["response"]["results"])

    # Stop when you reach the last page
    if data["response"]["currentPage"] >= data["response"]["pages"]:
        break

    page += 1

print("Finished fetching all pages.")
