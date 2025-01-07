"""
Module for generating context data for GitHub statistics.

Functions:
    get_context(username: str, token: str, year: int, time_zone: str) -> dict:
        Generate context data for the given year from the provided data.
"""

import calendar
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta
from itertools import groupby

import pytz

from log.logging_config import setup_logging
from util.fetch_data import get_gitlab_info

setup_logging()

def _parse_time(time_str: str, timezone: pytz.BaseTzInfo):
    """
    Parse the time string to the timezone.

    Args:
        time_str (str): The time string.
        timezone (pytz.BaseTzInfo): The timezone.

    Returns:
        str: The time string in the timezone.
    """
    result = None
    try:
        result = (
            datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            .replace(tzinfo=pytz.UTC)
            .astimezone(timezone)
        )
    except ValueError as e:
        logging.error("Failed to parse time: %s", e)
        logging.error("Time: %s", time_str)
        result = datetime(2000, 1, 1).isoformat()
    except pytz.UnknownTimeZoneError as e:
        logging.error("Unknown timezone: %s", e)
        result = datetime(2000, 1, 1).isoformat()

    return result


def _get_commit_type(message: str) -> str:
    """
    Get the type of the commit message based on the conventional commit types.

    Args:
        message (str): The commit message.

    Returns:
        str: The type of the commit message, including "feat", "fix", "docs", "style", "refactor",
             "test", "chore", "perf", "build", "revert", "ci", and "others".
    """
    commit_type = re.split(r"[:(!/\s]", message)[0].lower()
    conventional_types = {
        "feat": ["feature", "feat", "features", "feats"],
        "fix": ["fix"],
        "docs": ["docs", "doc", "documentation"],
        "style": ["style", "styles"],
        "refactor": ["refactor", "refactors", "refact"],
        "test": ["test", "tests"],
        "chore": ["chore", "chores"],
        "perf": ["perf", "performance"],
        "build": ["build", "builds"],
        "revert": ["revert"],
        "ci": ["ci", "cicd", "pipeline", "pipelines", "cd"],
    }
    for key, value in conventional_types.items():
        if commit_type in value:
            return key
    for key, value in conventional_types.items():
        for v in value:
            if v in message:
                return key
    return "others"



# TODO: GitHub -> GitLab
def get_context(baseurl:str,username: str, token: str, year: int, time_zone: str) -> dict:
    """
    Generate context data for the given year from the provided data.

    Args:
        username (str): The GitLab username.
        token (str): The GitLab access token.
        year (int): The year to generate the context data.
        time_zone (str): The timezone.

    Returns:
        dict: The context data.
    """

    logging.info("Generating context data for GitLab statistics...")

    data = get_gitlab_info(baseurl,username, token, year)

    # 结果字典

    # if "others" in commit_type_num:
    #     commit_type_num.pop("others", None)

    commit_type_num = data['contribution']['commit_type_num']

    language_in_repos_count = data['contribution']['language_counts']

    # Avatar URL
    avatar = data["basic"]["avatar_url"]
    # Username
    name = data["basic"]["name"]

    # Days since account creation
    created_time = data["basic"]["existdays"]

    # Number of followers
    followers_num = data["basic"]["followers"]
    # Number of following
    following_num = data["basic"]["followings"]

    # Number of stargazers
    stars_num = sum(detail["stargazerCount"] for _, detail in data["repo"].items())

    # Number of commits
    commits_num = data["contribution"]["commit_num"]
    # Number of issues
    issues_num = data["contribution"]["issue_num"]
    # Number of pull requests
    prs_num = data["contribution"]["mr_num"]

    # Number of repositories
    repos_num = len(data["repo"])
    # Top 3 most committed repositories
    top_3_most_committed_repos = sorted(
        [
            {"name": repo, "num": len(detail["commits"])}
            for repo, detail in data["repo"].items()
        ],
        key=lambda x: x["num"],
        reverse=True,
    )[: min(3, repos_num)]

    # Number of languages used in new repositories
    languages_num = len(language_in_repos_count)

    # Top 3 languages used in new repositories
    top_3_languages_used_in_repos = sorted(
        [{"name": k, "num": v} for k, v in language_in_repos_count.items()],
        key=lambda x: x["num"],
        reverse=True,
    )[: min(3, languages_num)]

    # Number of conventional commits
    conventional_commits_num = sum(commit_type_num.values())

    # Top 3 conventional commit types
    top_3_conventional_commit_types = sorted(
        [{"name": k, "num": v} for k, v in commit_type_num.items()],
        key=lambda x: x["num"],
        reverse=True,
    )[: min(3, len(commit_type_num))]

    return {
        "avatar": avatar,
        "year": year,
        "username": username,
        "name": name,
        "created_time": created_time,
        "followers_num": followers_num,
        "following_num": following_num,
        "stars_num": stars_num,
        "commits_per_day": data["contribution"]['commits_per_day'],
        "commits_days_num": data["contribution"]["commits_days_num"],
        "longest_commit_streak": data["contribution"]["longest_commit_streak"],
        "longest_commit_break": data["contribution"]["longest_commit_break"],
        "max_commits_per_day": data["contribution"]["max_date_occurrences"],
        "commits_per_month": data["contribution"]["commits_per_month"],
        "most_active_month": data["contribution"]["most_active_month"],
        "commits_per_weekday": data["contribution"]["commits_per_weekday"],
        "most_active_weekday": data["contribution"]["most_active_weekday"],
        "commits_per_hour": data["contribution"]["commits_per_hour"],
        "most_active_hour": data["contribution"]["most_active_hour"],
        "commits_num": commits_num,
        "issues_num": issues_num,
        "prs_num": prs_num,
        "repos_num": repos_num,
        "top_3_most_committed_repos": top_3_most_committed_repos,
        "languages_num": languages_num,
        "top_3_languages_used_in_repos": top_3_languages_used_in_repos,
        "conventional_commits_num": conventional_commits_num,
        "top_3_conventional_commit_types": top_3_conventional_commit_types,
    }
