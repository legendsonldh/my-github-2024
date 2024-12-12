import os
from dotenv import load_dotenv

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

if __name__ == "__main__":
    load_constants("WCY-dt", 2024)

    try:
        github = Github(access_token=ACCESS_TOKEN, username=USERNAME, timezone=TIMEZONE)
        # origin_data = github \
        #     .fetch_data() \
        #     .write_to_file("origin.json")

        key = {
            "account_info": {
                "url": "str",
                "name": "str",
                "username": "str",
                "avatar_url": "str",
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

        result = github \
            .read_from_file("origin.json") \
            .filter_all(year=YEAR) \
            .sort_all() \
            .count_all() \
            .write_to_file("result0.json")

        github.read_from_file("origin.json") \
            .filter_all(year=YEAR) \
            .sort_all() \
            .count_all() \
            .filter_json(key) \
            .write_to_file("result.json")

    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("Fetched successfully!")
