"""
This module contains functions to fetch and process GitHub data.

Functions:
    fetch_github(github: object, year: int, skip_fetch: bool = False) -> tuple:
        Fetches and processes GitHub data for a given year.
"""

import logging

from log.logging_config import setup_logging

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


def fetch_github(github: object, year: int, skip_fetch: bool = False) -> tuple:
    """
    Fetches and processes GitHub data for a given year.

    Args:
        github (object): GitHub object.
        year (int): Year to fetch data for.
        skip_fetch (bool): Skip fetching data from GitHub.

    Returns:
        tuple: Processed data.
    """
    origin = None
    data = None
    data_new_repo = None

    try:
        if not skip_fetch:
            origin = github.fetch_data(year=year).result

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

    except (ValueError, TypeError, KeyError) as e:
        logging.error("Error fetching data from GitHub: %s", e)
        return None, None

    logging.info("data: %s", data)
    logging.info("data_new_repo: %s", data_new_repo)
    logging.info("Data fetched successfully")
    return data, data_new_repo
