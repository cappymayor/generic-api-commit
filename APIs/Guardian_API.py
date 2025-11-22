import os

import pandas as pd
import requests

"""For the fetching part"""

url = "https://content.guardianapis.com/search"
api_key = os.getenv("GUARDIAN_API_KEY")
results_list = []
currentpage = 1
pages = 3

"""For the pagination part"""

while currentpage <= pages:
    parameters = {
        "api-key": api_key,
        "orderBy": "newest",
        "page-size": 50,
        "page": currentpage,
        "q": "Ukraine Russian War",
        # "from-date": "2025-11-11",
        # "end-date": "2025-11-12"
    }

    data = requests.get(url, params=parameters)
    data = data.json()

    print(f"STATUS (page {currentpage}):", data["response"]["status"])

    if data["response"]["status"] == "ok":
        print("We are on point")

        results = data["response"]["results"]
        print("Results on this page:", len(results))
        results_list.append(results)

    print("fetched", currentpage, "/", pages)

    currentpage += 1  # This is what increases it
    # currrentpage number to the next
    # pages = data["response"]["pages"]
    # i limited it to 3 up there so i can test with shorter length

num_of_result = len(results_list)
print("\nTOTAL RESULTS COLLECTED:", num_of_result)

print(results_list)
# I needed to see that the overall
# list itself contains actual values

flattened_file = pd.json_normalize(
    results_list
)

print(flattened_file)  # My final output that can be used for analysis.

# what if i want to view the results in each page:
page1 = results_list[0]
page2 = results_list[1]
page3 = results_list[2]

print("\nThe content of Page 1 is", page1)
