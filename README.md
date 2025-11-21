# Guardian API News Scraper
This project collects news articles from The Guardian Open Platform API based on a search query and date range. The script handles pagination, extracts relevant article information, and saves the final dataset as a CSV file for analysis.

## Features
- Fetches articles using The Guardian REST API

- Handles multi-page responses via pagination

- Normalizes JSON data into a pandas DataFrame

- Exports article metadata to a CSV file

## How It Works

1. Sends `GET` requests to the Guardian API using your API key.

2. Iterates through all pages of search results.

3. Extracts article details (headline, URL, publication date, section, etc.).

4. Stores results in a Python list and converts them into a pandas DataFrame.

5. Saves the final dataset to `data/Russ_Ukr_war_Update.csv`.


## Requirements

- Python

- `requests`

- `pandas`

You must store your API key in a filed name `access_key.py`
api_key = "YOUR_API_KEY"

## Usage
Run the script from your terminal
`python api_data_extractor.py`