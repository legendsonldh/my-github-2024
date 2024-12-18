"""
This module contains functions to count the number of commits, types of commits, repositories,
languages, stargazers, forks, pull requests, merged pull requests, and issues in the data.

Functions:
    _get_commit_type(message: str) -> str:
        Get the type of the commit message based on the conventional commit types.
    commits_number(data: dict) -> dict:
        Count the number of commits in the data.
    commits_types_number(data: dict) -> dict:
        Count the number of commits of each type in the data.
    commits_monthly_number(data: dict) -> dict:
        Count the number of commits in each month in the data.
    commits_weekdaily_number(data: dict) -> dict:
        Count the number of commits in each weekday in the data.
    commits_daily_number(data: dict) -> dict:
        Count the number of commits in each day in the data.
    commits_hourly_number(data: dict) -> dict:
        Count the number of commits in each hour in the data.
    repos_number(data: dict) -> dict:
        Count the number of repositories in the data.
    repos_languages_number(data: dict) -> dict:
        Count the number of repositories using each language in the data.
    repos_stargazer_number(data: dict) -> dict:
        Count the number of stargazers in the data.
    repos_fork_number(data: dict) -> dict:
        Count the number of forks in the data.
    prs_number(data: dict) -> dict:
        Count the number of pull requests in the data.
    prs_merged_number(data: dict) -> dict:
        Count the number of merged pull requests in the data.
    issues_number(data: dict) -> dict:
        Count the number of issues in the data.
"""

import re
from datetime import datetime, timedelta


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


def commits_number(data: dict) -> dict:
    """
    Count the number of commits in the data.

    Args:
        data (dict): The data containing the commits details.

    Returns:
        dict: The data containing the number of commits.
    """
    commits_num = 0
    for repo in data["repos_details"]:
        repo["commits_num"] = len(repo["commits_details"])
        commits_num += len(repo["commits_details"])

    data["commits_num"] = commits_num

    return data


def commits_types_number(data: dict) -> dict:
    """
    Count the number of commits of each type in the data.

    Args:
        data (dict): The data containing the commits details.

    Returns:
        dict: The data containing the number of commits of each type.
    """
    commits_types = {}
    for repo in data["repos_details"]:
        repo_commits_types = {}
        for commit in repo["commits_details"]:
            commit_type = _get_commit_type(commit["message"])

            if commit_type in repo_commits_types:
                repo_commits_types[commit_type] += 1
            else:
                repo_commits_types[commit_type] = 1

        repo["commits_types_num"] = repo_commits_types

        for key, value in repo_commits_types.items():
            if key in commits_types:
                commits_types[key] += value
            else:
                commits_types[key] = value

    data["commits_types_num"] = commits_types

    return data


def _count_monthly(items: list, key: str) -> dict:
    monthly_count = {}
    for item in items:
        month = datetime.fromisoformat(item[key]).month
        if month in monthly_count:
            monthly_count[month] += 1
        else:
            monthly_count[month] = 1
    return monthly_count


def _fill_monthly_list(monthly_count: dict) -> list:
    monthly_list = []
    for i in range(1, 13):
        if i in monthly_count:
            monthly_list.append(monthly_count[i])
        else:
            monthly_list.append(0)
    return monthly_list


def commits_monthly_number(data: dict) -> dict:
    """
    Count the number of commits in each month in the data.

    Args:
        data (dict): The data containing the commits details.

    Returns:
        dict: The data containing the number of commits in each month.
    """
    commits_monthly = _count_monthly(data["repos_details"], "created_time")

    for repo in data["repos_details"]:
        repo_commits_monthly = _count_monthly(repo["commits_details"], "created_time")
        repo["commits_monthly_num"] = _fill_monthly_list(repo_commits_monthly)

    commits_monthly.update(_count_monthly(data["prs_details"], "created_time"))
    commits_monthly.update(_count_monthly(data["issues_details"], "created_time"))

    data["commits_monthly_num"] = _fill_monthly_list(commits_monthly)

    return data


def _count_weekly(items: list, key: str) -> dict:
    weekly_count = {}
    for item in items:
        weekday = datetime.fromisoformat(item[key]).weekday()
        if weekday in weekly_count:
            weekly_count[weekday] += 1
        else:
            weekly_count[weekday] = 1
    return weekly_count


def _fill_weekly_list(weekly_count: dict) -> dict:
    weekly_list = []
    for i in range(7):
        if i in weekly_count:
            weekly_list.append(weekly_count[i])
        else:
            weekly_list.append(0)
    return weekly_list


def commits_weekdaily_number(data: dict) -> dict:
    """
    Count the number of commits in each weekday in the data.

    Args:
        data (dict): The data containing the commits details.

    Returns:
        dict: The data containing the number of commits in each weekday.
    """
    commits_weekly = {}

    for repo in data["repos_details"]:
        repo_commits_weekly = _count_weekly(repo["commits_details"], "created_time")
        repo["commits_weekdaily_num"] = _fill_weekly_list(repo_commits_weekly)
        for weekday, count in repo_commits_weekly.items():
            if weekday in commits_weekly:
                commits_weekly[weekday] += count
            else:
                commits_weekly[weekday] = count

    commits_weekly.update(_count_weekly(data["prs_details"], "created_time"))
    commits_weekly.update(_count_weekly(data["issues_details"], "created_time"))

    data["commits_weekdaily_num"] = _fill_weekly_list(commits_weekly)

    return data


def _count_daily(items: list, key: str) -> dict:
    daily_count = {}
    for item in items:
        date = datetime.fromisoformat(item[key]).date().isoformat()
        if date in daily_count:
            daily_count[date] += 1
        else:
            daily_count[date] = 1
    return daily_count


def _fill_daily_list(daily_count: dict) -> dict:
    daily_list = {}
    for year in range(2000, datetime.now().year + 2):
        days_in_year = (
            366 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 365
        )
        tmp = []
        for day in range(days_in_year):
            date = (datetime(year, 1, 1) + timedelta(days=day)).date().isoformat()
            if date in daily_count:
                tmp.append(daily_count[date])
            else:
                tmp.append(0)
        if sum(tmp) != 0:
            daily_list[year] = tmp
    return daily_list


def commits_daily_number(data: dict) -> dict:
    """
    Count the number of commits in each day in the data.

    Args:
        data (dict): The data containing the commits details.

    Returns:
        dict: The data containing the number of commits in each day.
    """
    commits_daily = _count_daily(data["repos_details"], "created_time")

    for repo in data["repos_details"]:
        repo_commits_daily = _count_daily(repo["commits_details"], "created_time")
        repo["commits_daily_num"] = _fill_daily_list(repo_commits_daily)
        for date, count in repo_commits_daily.items():
            if date in commits_daily:
                commits_daily[date] += count
            else:
                commits_daily[date] = count

    commits_daily.update(_count_daily(data["prs_details"], "created_time"))
    commits_daily.update(_count_daily(data["issues_details"], "created_time"))

    data["commits_daily_num"] = _fill_daily_list(commits_daily)

    return data


def _count_hourly(items: list, key: str) -> dict:
    hourly_count = {}
    for item in items:
        hour = datetime.fromisoformat(item[key]).hour
        if hour in hourly_count:
            hourly_count[hour] += 1
        else:
            hourly_count[hour] = 1
    return hourly_count


def _fill_hourly_list(hourly_count: dict) -> list:
    hourly_list = []
    for i in range(24):
        if i in hourly_count:
            hourly_list.append(hourly_count[i])
        else:
            hourly_list.append(0)
    return hourly_list


def commits_hourly_number(data: dict) -> dict:
    """
    Count the number of commits in each hour in the data.

    Args:
        data (dict): The data containing the commits details.

    Returns:
        dict: The data containing the number of commits in each hour.
    """
    commits_hourly = {}

    for repo in data["repos_details"]:
        repo_commits_hourly = _count_hourly(repo["commits_details"], "created_time")
        repo["commits_hourly_num"] = _fill_hourly_list(repo_commits_hourly)
        for hour, count in repo_commits_hourly.items():
            if hour in commits_hourly:
                commits_hourly[hour] += count
            else:
                commits_hourly[hour] = count

    commits_hourly.update(_count_hourly(data["prs_details"], "created_time"))
    commits_hourly.update(_count_hourly(data["issues_details"], "created_time"))

    data["commits_hourly_num"] = _fill_hourly_list(commits_hourly)

    return data


def repos_number(data: dict) -> dict:
    """
    Count the number of repositories in the data.

    Args:
        data (dict): The data containing the repositories details.

    Returns:
        dict: The data containing the number of repositories.
    """
    repos_num = len(data["repos_details"])
    data["repos_num"] = repos_num

    return data


def repos_languages_number(data: dict) -> dict:
    """
    Count the number of repositories using each language in the data.

    Args:
        data (dict): The data containing the repositories details.

    Returns:
        dict: The data containing the number of repositories using each language.
    """
    languages_num = {}
    repos_languages_count = {}
    for repo in data["repos_details"]:
        for key, value in repo["languages_num"].items():
            if key in languages_num:
                languages_num[key] += value
                repos_languages_count[key] += 1
            else:
                languages_num[key] = value
                repos_languages_count[key] = 1

        repo["languages_num"] = dict(
            sorted(repo["languages_num"].items(), key=lambda x: x[1], reverse=True)
        )

    data["languages_num"] = languages_num
    data["languages_num"] = dict(
        sorted(data["languages_num"].items(), key=lambda x: x[1], reverse=True)
    )

    data["repos_languages_num"] = repos_languages_count
    data["repos_languages_num"] = dict(
        sorted(data["repos_languages_num"].items(), key=lambda x: x[1], reverse=True)
    )

    return data


def repos_stargazer_number(data: dict) -> dict:
    """
    Count the number of stargazers in the data.

    Args:
        data (dict): The data containing the repositories details.

    Returns:
        dict: The data containing the number of stargazers.
    """
    stargazers_num = 0
    for repo in data["repos_details"]:
        stargazers_num += repo["stargazers_num"]

    data["stargazers_num"] = stargazers_num

    return data


def repos_fork_number(data: dict) -> dict:
    """
    Count the number of forks in the data.

    Args:
        data (dict): The data containing the repositories details.

    Returns:
        dict: The data containing the number of forks.
    """
    forks_num = 0
    for repo in data["repos_details"]:
        forks_num += repo["forks_num"]

    data["forks_num"] = forks_num

    return data


def prs_number(data: dict) -> dict:
    """
    Count the number of pull requests in the data.

    Args:
        data (dict): The data containing the pull requests details.

    Returns:
        dict: The data containing the number of pull requests.
    """
    prs_num = len(data["prs_details"])
    data["prs_num"] = prs_num

    return data


def prs_merged_number(data: dict) -> dict:
    """
    Count the number of merged pull requests in the data.

    Args:
        data (dict): The data containing the pull requests details.

    Returns:
        dict: The data containing the number of merged pull requests.
    """
    merged_prs_number = len(list(filter(lambda x: x["merged"], data["prs_details"])))
    data["prs_merged_num"] = merged_prs_number

    return data


def issues_number(data: dict) -> dict:
    """
    Count the number of issues in the data.

    Args:
        data (dict): The data containing the issues details.

    Returns:
        dict: The data containing the number of issues.
    """
    issues_num = len(data["issues_details"])
    data["issues_num"] = issues_num

    return data
