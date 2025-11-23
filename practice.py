# I import csv from Python’s standard library to save data into a CSV file
import csv

# I import requests to make HTTP requests to the Guardian API
import requests

# I store the API key to authenticate requests and the base URL of the Guardian API
# In production, I would store the API key in environment variables instead of hardcoding it
API_KEY = "e58deace-2a4d-4355-8b07-f225eaf5b467"
BASE_URL = "https://content.guardianapis.com/search"

def fetch_all_articles(query):
   """
    This function accepts a search query and fetches all articles from the Guardian API.
    It handles pagination, errors, and returns a complete list of articles.
    """
    # I start at page 1 and initialize an empty list to store all results
    page = 1
    all_results = []

    # I loop until all pages are fetched
    while True:
        try:
            # I define the parameters for the API request:
            # query, API key, page number, page size, and the fields I want (headline, bodyText)
            params = {
                "q": query,
                "api-key": API_KEY,
                "page": page,
                "page-size": 50,
                "show-fields": "headline,bodyText",
            }

            # I send a GET request to the Guardian API with the parameters and a 10-second timeout
            # The response is stored in the variable 'response'
            response = requests.get(BASE_URL, params=params, timeout=10)

            # I check if the request was successful; if not, an exception is raised
            response.raise_for_status()

            # I convert the JSON response into a Python dictionary for easier access
            data = response.json()

            # The articles are stored inside data["response"]["results"], so I extract them
            results = data["response"]["results"]

            # I add all articles from this page to my main list of all results
            all_results.extend(results)

            # I print the current page number to track progress
            print(f"Fetched page {page}")

            # If the current page is the last page, I break the loop
            if page >= data["response"]["pages"]:
                break

            # Otherwise, I move to the next page
            page += 1

        # If any request-related error occurs, I print the error and stop the loop
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            break

    # After fetching all pages, I return the complete list of articles
    return all_results

# I call the function with my search query and store the results in 'articles'
articles = fetch_all_articles("Russia Ukraine war")

# I print the total number of articles fetched
print(f"Total articles fetched: {len(articles)}")

# I define the CSV file name where I want to save the articles
csv_file = "russia_ukraine_articles.csv"

# I open the CSV file in write mode with UTF-8 encoding
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    # I create a CSV writer object
    writer = csv.writer(file)

    # I write the header row of the CSV file
    writer.writerow(["Headline", "Body"])

    # I loop through each article and write the headline and body text
    # I use .get() to avoid errors if a field is missing
    for article in articles:
        headline = article.get("fields", {}).get("headline", "")
        body = article.get("fields", {}).get("bodyText", "")
        writer.writerow([headline, body])

# I print a message confirming the CSV file has been saved
print(f"Articles saved to {csv_file}")
