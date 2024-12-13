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

def fetch_github(github, year: int, skip_fetch: bool = False):
    try:
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
            .filter_json(key=KEY) \
            .write_to_file("data/result_new_repo.json")

    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("Fetched successfully!")
