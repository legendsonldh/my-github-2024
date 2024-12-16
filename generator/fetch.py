from log.logging_config import setup_logging
import logging

setup_logging()

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


def fetch_github(github, year, skip_fetch = False):
    origin = None
    data = None
    data_new_repo = None

    try:
        if not skip_fetch:
            origin = github.fetch_data().result

        github.result = origin
        data = (
            github.filter_all(year=year)
            .sort_all()
            .count_all()
            .filter_json(key=KEY)
            .result
        )

        github.result = origin
        data_new_repo = (
            github.filter_all(year=year)
            .filter_repos(year=year)
            .sort_all()
            .count_all()
            .filter_json(key=KEY_NEW_REPO)
            .result
        )

    except Exception as e:
        logging.error(f"Error fetching data from GitHub: {e}")
        return None, None
    else:
        logging.info(f"data: {data}")
        logging.info(f"data_new_repo: {data_new_repo}")
        logging.info("Data fetched successfully")
        return data, data_new_repo
