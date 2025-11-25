import requests

API_KEY = "a58745b1-8abb-49da-837f-aee926c7f227"
url = " https://content.guardianapis.com/search"

parameter = {
    "q": "fashion",
    "order-by": "relevance",
    "page": 1,
    "from-date": "2025-09-01",
    "to-date": "2025-11-2",
    "api-key": API_KEY
}


def page_extraction():
    page = 1
    count_page = 1
    fashion = []

    while page <= count_page:
        parameter["page"] = page
        response = requests.get(
            url="https://content.guardianapis.com/search",
            params=parameter
        )

        if response.status_code != 200:
            response.raise_for_status()

        data = response.json()
        pages = data['response']['pages']
        print(f"The number of pages are {pages}")

        for style in data["response"]["results"]:
            fashion.append(style)

            page += 1

    return fashion


result = page_extraction()
print(f"The result are {result}")
