import requests

url = "https://content.guardianapis.com/search"
params = {
    "q": "Russia-Ukraine war",
    "from-date": "2024-01-01",
    "to-date": "2025-01-05",
    "api-key": "24398a76-63e3-496d-9d9c-a0ce71f21ce7"
}

page = 1

while True:
    params["page"] = page

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Request failed: {e}")
        break

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
