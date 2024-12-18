"""
Module for generating context data for GitHub statistics.

Functions:
    get_context(year: int, data: dict, data_new_repo: dict) -> dict:
        Generate context data for the given year from the provided data.
"""

from itertools import groupby

def get_context(year: int, data: dict, data_new_repo: dict) -> dict:
    """
    Generate context data for the given year from the provided data.

    Args:
        year (int): The year for which to generate the context.
        data (dict): The data containing GitHub statistics.
        data_new_repo (dict): The data containing new repository statistics.

    Returns:
        dict: A dictionary containing the generated context data.
    """
    avatar = data["account_info"]["avatar"]
    username = data["account_info"]["username"]
    name = data["account_info"]["name"]
    created_time = (int(data["account_info"]["created_time"]) + 99) // 100 * 100
    followers_num = data["account_info"]["followers_num"]
    following_num = data["account_info"]["following_num"]
    stars_num = data["stargazers_num"]

    commits_per_day = data["commits_daily_num"][year]
    commits_days_num = len([x for x in commits_per_day if x > 0])
    longest_commit_streak = max(
        (len(list(g)) for k, g in groupby(commits_per_day, key=lambda x: x > 0) if k),
        default=0,
    )
    longest_commit_break = max(
        (len(list(g)) for k, g in groupby(commits_per_day, key=lambda x: x == 0) if k),
        default=0,
    )
    max_commits_per_day = max(commits_per_day)

    commits_per_month = data["commits_monthly_num"]
    most_active_month = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ][commits_per_month.index(max(commits_per_month))]
    commits_per_weekday = data["commits_weekdaily_num"]
    most_active_weekday = [
        "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
    ][commits_per_weekday.index(max(commits_per_weekday))]
    commits_per_hour = data["commits_hourly_num"]
    most_active_hour = [f"{i}:00" for i in range(24)][
        commits_per_hour.index(max(commits_per_hour))
    ]

    commits_num = data["commits_num"]
    issues_num = data["issues_num"]
    prs_num = data["prs_num"]

    repos_num = data["repos_num"]
    top_3_most_committed_repos = sorted(
        [{"name": repo["name"], "num": repo["commits_num"]} for repo in data["repos_details"]],
        key=lambda x: x["num"],
        reverse=True,
    )[: min(3, len(data["repos_details"]))]
    languages_num = len(data_new_repo["languages_num"])
    top_3_languages_used_in_new_repos = list(
        {"name": k, "num": v} for k, v in data_new_repo["languages_num"].items()
    )[: min(3, len(data_new_repo["languages_num"]))]
    conventional_commits_num = sum(
        v for k, v in data["commits_types_num"].items() if k != "others"
    )
    top_3_conventional_commit_types = sorted(
        [{"name": k, "num": v} for k, v in data["commits_types_num"].items() if k != "others"],
        key=lambda x: x["num"],
        reverse=True,
    )[: min(3, len(data["commits_types_num"]) - 1)]

    return {
        "avatar": avatar,
        "year": year,
        "username": username,
        "name": name,
        "created_time": created_time,
        "followers_num": followers_num,
        "following_num": following_num,
        "stars_num": stars_num,
        "commits_per_day": commits_per_day,
        "commits_days_num": commits_days_num,
        "longest_commit_streak": longest_commit_streak,
        "longest_commit_break": longest_commit_break,
        "max_commits_per_day": max_commits_per_day,
        "commits_per_month": commits_per_month,
        "most_active_month": most_active_month,
        "commits_per_weekday": commits_per_weekday,
        "most_active_weekday": most_active_weekday,
        "commits_per_hour": commits_per_hour,
        "most_active_hour": most_active_hour,
        "commits_num": commits_num,
        "issues_num": issues_num,
        "prs_num": prs_num,
        "repos_num": repos_num,
        "top_3_most_committed_repos": top_3_most_committed_repos,
        "languages_num": languages_num,
        "top_3_languages_used_in_new_repos": top_3_languages_used_in_new_repos,
        "conventional_commits_num": conventional_commits_num,
        "top_3_conventional_commit_types": top_3_conventional_commit_types,
    }
