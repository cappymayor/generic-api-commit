import pandas as pd
import requests

import access_key

url = "https://content.guardianapis.com/search"
current_page = 1
total_pages = 1

container = []

while current_page <= total_pages:
    params ={
    "api-key": access_key.api_key,
    "q": "Russia Ukraine",
    "from-date": "2025-10-11",
    "to-date": "2025-10-20",
    "page": current_page
    
    }
    
    response = requests.get(url=url, params=params)
    
    if response.status_code != 200:
        print(response.raise_for_status())
        break
        
    else:
        full = response.json()
        total_pages = full['response']['pages']
        
        
        total_results = full['response']['results']
        for data in total_results:
            container.append(data)
        
        
        current_page += 1
        
print(f"Total recored processed: {len(container)}")

df = pd.json_normalize(container)
df.to_csv("data/Russ_Ukr_war_Update.csv")
