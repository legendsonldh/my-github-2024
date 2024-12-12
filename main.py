import os
from dotenv import load_dotenv
import json

from src.github import Github

def load_constants(username: str, year: int):
    global ACCESS_TOKEN
    load_dotenv()
    ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

    global USERNAME
    USERNAME = username

    global YEAR
    YEAR = year

    global TIMEZONE
    TIMEZONE = "Asia/Shanghai"

    global KEY
    KEY = {
        "account_info": {
            "url": "str",
            "name": "str",
            "username": "str",
            "avatar": "str",
            "bio": "str",
            "followers_num": "int",
            "following_num": "int",
            "created_time": "str",
        },
        "repos_details": {
            "url": "str",
            "name": "str",
            "description": "str",
            "created_time": "str",
            "commits_num": "int",
            "languages_num": "dict",
            "stargazers_num": "int",
            "forks_num": "int",
            "commits_monthly_num": "dict",
        },
        "repos_num": "int",
        "commits_num": "int",
        "commits_types_num": "dict",
        "commits_monthly_num": "dict",
        "commits_weekdaily_num": "dict",
        "commits_daily_num": "dict",
        "commits_hourly_num": "dict",
        "issues_num": "int",
        "forks_num": "int",
        "stars_num": "int",
        "prs_num": "int",
        "prs_merged_num": "int",
        "stargazers_num": "int",
        "languages_num": "dict",
        "repos_languages_num": "dict",
    }

if __name__ == "__main__":
    load_constants("WCY-dt", 2024)

    try:
        github = Github(access_token=ACCESS_TOKEN, username=USERNAME, timezone=TIMEZONE)
        # origin_data = github \
        #     .fetch_data() \
        #     .write_to_file("origin.json")

        github.read_from_file("origin.json") \
            .filter_all(year=YEAR) \
            .sort_all() \
            .count_all() \
            .filter_json(key=KEY) \
            .write_to_file("result.json")
        
        github.read_from_file("origin.json") \
            .filter_all(year=YEAR) \
            .filter_repos(year=YEAR) \
            .sort_all() \
            .count_all() \
            .filter_json(key=KEY) \
            .write_to_file("result_new_repo.json")

    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("Fetched successfully!")

    data = None
    with open("result.json", "r") as f:
        data = json.load(f)
    data_new_repo = None
    with open("result_new_repo.json", "r") as f:
        data_new_repo = json.load(f)

    USERNAME = data["account_info"]["username"]
    NAME = data["account_info"]["name"]
    AVATAR = data["account_info"]["avatar"]
    BIO = data["account_info"]["bio"]
    CREATED_TIME = data["account_info"]["created_time"]

    FOLLOWERS_NUM = data["account_info"]["followers_num"]
    FOLLOWING_NUM = data["account_info"]["following_num"]

    COMMITS_NUM = data["commits_num"]
    COMMITS_TYPES_NUM = data["commits_types_num"]
    COMMITS_PER_MONTH = data["commits_monthly_num"]
    COMMITS_PER_WEEKDAY = data["commits_weekdaily_num"]
    COMMITS_PER_DAY = data["commits_daily_num"]
    COMMITS_PER_HOUR = data["commits_hourly_num"]
    MOST_COMMITTED_REPO = data["repos_details"][0]["name"]
    COMMITS_NUM_OF_MOST_COMMITTED_REPO = data["repos_details"][0]["commits_num"]

    REPOS_NUM = data["repos_num"]
    NEW_REPOS_NUM = data_new_repo["repos_num"]

    NUMBER_OF_LANGUAGES_USED_IN_NEW_REPOS = len(data_new_repo["repos_languages_num"])
    MOST_USED_LANGUAGE_IN_NEW_REPOS = list(data_new_repo["repos_languages_num"].keys())[0]
    TOP_3_LANGUAGES_USED_IN_NEW_REPOS = list(data_new_repo["repos_languages_num"].keys())[:min(3, len(data_new_repo["repos_languages_num"]))]

    COMMITS_NUM = data["commits_num"]



