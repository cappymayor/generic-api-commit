import time

import requests

import access_key


def fetch_all_guardian_data(query="Russian OR Ukraine"):


    base_url = "https://content.guardianapis.com/search"
    all_results = []

    params = {
        "q": query,
        "api-key": access_key.api_key,
        "page": 1,        
        "page-size": 50
    }

    total_pages = 1       
    current_page = 1      # loop counter

    print(f"Starting data retrieval for query: '{query}'")


    while current_page <= total_pages:
        params['page'] = current_page

        if current_page > 1:
            time.sleep(0.5) 

        print(f"Retrieving page {current_page}...")

        try:
            r = requests.get(base_url, params=params)
            r.raise_for_status() 
            page_data = r.json()

            response = page_data['response']

            if current_page == 1:
                total_pages = response.get('pages', 1)
                print(f"Discovered total pages: {total_pages}")


            all_results.extend(response.get('results', []))


            current_page += 1

        except requests.exceptions.RequestException as error:
            print(f"Request failed on page {current_page}: {error}.")
            break 

    print(f"\nFinished retrieval! Total articles collected: {len(all_results)}")
    return all_results

if __name__ == '__main__':
    print("Running extractor directly.")
    data = fetch_all_guardian_data()
