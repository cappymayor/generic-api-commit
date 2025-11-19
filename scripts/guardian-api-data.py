import argparse
import json
import os

import pandas as pd
import requests
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

argparser = argparse.ArgumentParser(
    description="The Guardian API Data Extraction"
    )
argparser.add_argument(
    "--params",
    type=str,
    help="Path to a JSON file containing parameters for The Guardian API"
    )

argparser.add_argument(
    "--max_pages",
    type=str,
    default=None,
    help="Max pages to be processed by the script"
    )


# Extract all pages from the URL and return as a pandas DataFrame
# after selecting fields of interest
def get_articles_dataframe(
    base_url, api_key, request_parameters, max_pages=None
):
    """
    Fetch articles from The Guardian API and return as a pandas DataFrame.

    Args:
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        query (str): The search query.
        page_size (int): Number of articles per page.
        max_pages (int, optional): Maximum number of pages to fetch.

    Returns:
        pd.DataFrame: A DataFrame containing the articles.
    """
    all_articles = []
    page = 1
    while True:
        params = request_parameters.copy()
        params["page"] = page
        url = f"{base_url}?api-key={api_key}"
        try:
            response = requests.get(url, params=params)
        except Exception as e:
            print(f"An error occurred while making the request: {e}")
            raise
        if response.status_code != 200:
            print(f"API request failed with status {response.status_code}")
            break

        max_page = response.json().get("response", {}).get("pages", 0)
        if max_pages is not None and max_pages < max_page:
            max_page = max_pages
        data = response.json()
        articles = data.get("response", {}).get("results", [])
        if not articles:
            break

        for article in articles:
            fields = article.get("fields", {})
            formatted_article = {
                "headline": fields.get("headline", ""),
                "trailText": fields.get("trailText", ""),
                "byline": fields.get("byline", ""),
                "publication": fields.get("publication", ""),
                "webUrl": article.get("webUrl", ""),
                "webPublicationDate": article.get(
                    "webPublicationDate", ""
                ),
            }
            all_articles.append(formatted_article)

        print(f"Fetched page {page} of {max_page}")
        page += 1
        if page > max_page:
            break  # Exiting the loop if we've reached the max pages

    return pd.DataFrame(all_articles)


def load_params(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        raise
    except FileNotFoundError as e:
        print(f"File not found: {file_path}: {e}")
        raise


def main():
    args = argparser.parse_args()
    if not args.params:
        raise ValueError("The --params argument is required.")
    params = load_params(args.params)
    max_pages = args.max_pages
    if "config" not in params or "request_params" not in params:
        raise KeyError("The JSON file must contain a 'config' or "
                       "'request_params' key.")
    config = params["config"]
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY is not set in the environment variables.")

    df = get_articles_dataframe(
        base_url=config["base_url"],
        api_key=api_key,
        request_parameters=params["request_params"],
        max_pages=int(max_pages) if max_pages else None)
    print(df.head())


if __name__ == "__main__":
    main()
