import os

KEY = {
    "commits_daily_num": "dict",
    "account_info": {
        "avatar": "str",
        "url": "str",
        "name": "str",
        "username": "str",
        "followers_num": "int",
        "following_num": "int",
        "created_time": "str",
    },
    "stargazers_num": "int",
    "commits_monthly_num": "dict",
    "commits_weekdaily_num": "dict",
    "commits_hourly_num": "dict",
    "commits_num": "int",
    "issues_num": "int",
    "prs_num": "int",
    "repos_num": "int",
    "repos_details": {
        "name": "str",
        "commits_num": "int",
    },
    "commits_types_num": "dict",
}

KEY_NEW_REPO = {
    "languages_num": "dict",
}

def fetch_github(github, year: int, skip_fetch: bool = False) -> None:
    try:
        if not os.path.exists("data"):
            os.makedirs("data")

        if not skip_fetch:
            github \
                .fetch_data() \
                .write_to_file("data/origin.json")

        github \
            .read_from_file("data/origin.json") \
            .filter_all(year=year) \
            .sort_all() \
            .count_all() \
            .filter_json(key=KEY) \
            .write_to_file("data/result.json")

        github \
            .read_from_file("data/origin.json") \
            .filter_all(year=year) \
            .filter_repos(year=year) \
            .sort_all() \
            .count_all() \
            .filter_json(key=KEY_NEW_REPO) \
            .write_to_file("data/result_new_repo.json")

    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("Fetched successfully!")
