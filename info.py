from src.basic import get_github_info

import requests
import json

if __name__ == "__main__":
    username = "WCY-dt"

    try:
        username = "WCY-dt"
        result = get_github_info(username)
        # print(json.dumps(result, indent=4))
        with open("info.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result, indent=4))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("Fetched successfully!")