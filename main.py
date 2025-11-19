import os

import pandas as pd

from api_data_extractor import fetch_all_guardian_data

OUTPUT_DIR = "/Users/makpro/Desktop/anything_engineering/generic-api-commit/data"
OUTPUT_FILENAME = 'Rosso_Ukr_war.csv'
FILE_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

def main():


    print("--- Starting Data Pipeline ---")


    all_article_data = fetch_all_guardian_data()
    
    if all_article_data:

        df = pd.DataFrame(all_article_data)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df.to_csv(FILE_PATH, index=False)

        print(f"\n--- Pipeline Complete ---")
        print(f"Total records processed: {len(df)}")
        print(f"Data saved successfully to: {FILE_PATH}")

    else:
        print("Data retrieval failed. Stopping pipeline.")

if __name__ == '__main__':
    main()
