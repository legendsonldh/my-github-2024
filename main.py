from src.filter import Filter

import requests
import os
import json
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

    username = "WCY-dt"

    YEAR = 2024

    try:
        filter = Filter(access_token=ACCESS_TOKEN, username=username)
        result = filter \
            .fetch_data() \
            .filter_year(YEAR) \
            .sort_all() \
            .count_all() \
            .result

        with open("info.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result, indent=4))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("Fetched successfully!")