"""
This module provides functions to fetch GitHub data using the GitHub GraphQL API.

Functions:
    get_github_info(username: str, token: str, year: int) -> dict:
        Get the GitHub information for the given year.
"""
import calendar
import logging
from datetime import datetime
from itertools import groupby

import gitlab
import pytz
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from log.logging_config import setup_logging
from collections import defaultdict, Counter
import util.context


setup_logging()


# Initialize the GitLab API client
def initialize_gitlab_client(baseurl:str,token: str):
    gl = gitlab.Gitlab(baseurl, oauth_token=token)
    return gl


# Fetch user information
def _get_basic(user_name: str, gl) -> dict:
    user = gl.users.list(username=user_name)[0]
    logging.info("Fetching GitLab basic data. %s", user)

    # Days since account creation
    existdays = (
        (
            (
                datetime.now(pytz.UTC)
                - datetime.strptime(user.created_at, "%Y-%m-%dT%H:%M:%S.%f%z")
            ).days
            + 99
        )
        // 100
        * 100
    )
    return {
        "id": user.id,
        "name": user.name,
        "avatar_url": user.avatar_url,
        "followers": len(user.followers_users.list()),
        "followings": len(user.following_users.list()),
        "created_time": user.created_at,
        "email": user.email,
        "existdays": existdays

    }

# Fetch repositories
def _get_repo(user_name: str,user_email:str, user_id: str, gl, year: int):
    projects = gl.projects.list(get_all=True,keep_base_url=True)
    all_repos = {}
    contribution_calendar = []
    commit_count = 0

    mr_count = 0
    issues_count = 0
    issues = []

    commit_type_num = defaultdict(int)
    commit_time_num = [0] * 24
    language_in_repos = []
    for project in projects:
        members = project.members.list(get_all=True)

        for member in members:
            if member.id == user_id:
                repo_name = project.name
                created_at = project.created_at
                # 如果仓库是在给定年份创建的，则获取该年份的提交记录
                commits = []
                user_commits = 0  # 统计该用户作为提交者的提交数量
                reviewer_commits = 0  # 统计该用户作为审核者的提交数量
                # 获取仓库的语言统计
                repo_languages = project.languages()
                language_in_repos.append(repo_languages)
                # 获取该仓库的提交记录
                commit_list = project.commits.list(ref_name = "develop",since=f'{year}-01-01T00:00:00Z', until=f'{year}-12-31T23:59:59Z',
                                                get_all=True,keep_base_url=True)

                user_identifiers = {user_name, user_email}
                for commit in commit_list:

                    commit_data = {
                        "message": commit.message,
                        "committedDate": commit.created_at,
                    }

                    # 判断该用户是否是提交者
                    if commit.author_name in user_identifiers or commit.author_email in user_identifiers:
                        commit_type = util.context._get_commit_type(commit_data["message"])
                        commit_type_num[commit_type] += 1

                        # 处理 commit_time
                        commit_time = util.context._parse_time(commit_data["committedDate"], pytz.timezone('Asia/Shanghai')).hour
                        commit_time_num[commit_time] += 1
                        contribution_calendar.append(commit.created_at[:10])

                        commits.append(commit_data)
                        user_commits += 1  # 作为提交者的提交数量


                    # 判断该用户是否是审核者（committer_name）
                    if commit.committer_name in user_identifiers or commit.committer_email in user_identifiers:
                        reviewer_commits += 1  # 作为审核者的提交数量

                commit_count += user_commits

                try:
                    # merge
                    created_at_merge_requests = project.mergerequests.list(scope="created_by_me", created_after=f'{year}-01-01',
                                                                     created_before=f'{year}-12-31',
                                                                     get_all=True)
                except gitlab.exceptions.GitlabError:
                    created_at_merge_requests = []

                try:
                    assigned_to_merge_requests = project.mergerequests.list(scope="assigned_to_me ", created_after=f'{year}-01-01',
                                                                     created_before=f'{year}-12-31',
                                                                     get_all=True)
                except gitlab.exceptions.GitlabError:
                    assigned_to_merge_requests = []


                mr_count += len(created_at_merge_requests)
                mr_count += len(assigned_to_merge_requests)

                try:
                    # merge
                    issues = project.issues.list(assignee_id=user_id, created_after=f'{year}-01-01',
                                                                     created_before=f'{year}-12-31',
                                                                     get_all=True)
                except gitlab.exceptions.GitlabError:
                    issues = []

                issues_count += len(issues)


                # 保存仓库的数据，包括用户作为提交者和审核者的统计
                all_repos[repo_name] = {
                    "stargazerCount": project.star_count,
                    "forkCount": project.forks_count,
                    "isPrivate": project.visibility == 'private',
                    "createdAt": created_at,
                    "languages": repo_languages,
                    "commits": commits,
                    "userCommits": user_commits,  # 该用户作为提交者的提交数量
                    "reviewerCommits": reviewer_commits,  # 该用户作为审核者的提交数量
                }
                # 后续相关代码逻辑
                break

    languages = [lang for item in language_in_repos if item for lang in item.keys()]
    language_counts = Counter(languages)

    # Number of activities in each day
    commits_per_day = contribution_calendar
    # Number of days with activities（活动天数，即不重复的日期数量）
    unique_days = len(set(commits_per_day))

    # Longest active streak（最长连续出现相同日期的天数，这里理解为同一天多次出现视为连续活动）
    date_groups = [(date, len(list(group))) for date, group in groupby(commits_per_day)]
    longest_commit_streak = max([count for _, count in date_groups]) if date_groups else 0

    # Longest inactive streak（最长连续不出现的天数间隔，这里通过比较相邻日期的差值来统计）
    sorted_dates = sorted(commits_per_day)
    date_gaps = []
    for i in range(len(sorted_dates) - 1):
        current_date = sorted_dates[i]
        next_date = sorted_dates[i + 1]
        from datetime import datetime
        current_date_obj = datetime.strptime(current_date, '%Y-%m-%d')
        next_date_obj = datetime.strptime(next_date, '%Y-%m-%d')
        gap = (next_date_obj - current_date_obj).days
        date_gaps.append(gap)
    longest_commit_break = max(date_gaps) if date_gaps else 0

    # Maximum number of occurrences of a date in a day（某一天出现的最大次数，也就是重复次数最多的日期的重复次数）
    date_counts = {}
    for date in commits_per_day:
        date_counts[date] = date_counts.get(date, 0) + 1
    max_date_occurrences = max(date_counts.values()) if date_counts else 0

    # 用于统计每个月活动数量的字典，键为月份（格式 '2023-01' 这样），值为活动数量

    days_in_year = 366 if calendar.isleap(year) else 365

    commits_per_year = [0] * days_in_year
    commits_per_weekday = [0] * 7
    commits_per_month = [0] * 12

    for date_str in commits_per_day:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        month = date_obj.month - 1
        day_of_year = date_obj.timetuple().tm_yday - 1
        commits_per_month[month] += 1
        commits_per_year[day_of_year] += 1
        weekday = date_obj.weekday()
        commits_per_weekday[weekday] += 1

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    most_active_month = month_names[commits_per_month.index(max(commits_per_month))]

    # Most active weekday（找出最活跃的工作日）
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    most_active_weekday = weekday_names[commits_per_weekday.index(max(commits_per_weekday))]

    # Most active hour（找出最活跃的小时）
    hour_formats = [f"{i}:00" for i in range(24)]
    most_active_hour = hour_formats[commit_time_num.index(max(commit_time_num))]


    contribution_info = {
            "mr_num": mr_count,
            "commit_num": commit_count,
            "issue_num":issues_count,
            "commit_type_num":commit_type_num,
            "commit_time_num": commit_time_num,
            "language_counts":language_counts,
            "commits_days_num":unique_days,
            "commits_per_day":commits_per_year,
            "longest_commit_streak":longest_commit_streak,
            "longest_commit_break":longest_commit_break,
            "max_date_occurrences":max_date_occurrences,
            "commits_per_month":commits_per_month,
            "most_active_month": most_active_month,
            "commits_per_weekday": commits_per_weekday,
            "most_active_weekday": most_active_weekday,
            "commits_per_hour": commit_time_num,
            "most_active_hour": most_active_hour,
        }

    return all_repos,contribution_info


# Main function to gather GitLab data
def get_gitlab_info(baseurl:str,username: str, token: str, year: int) -> dict:
    gl = initialize_gitlab_client(baseurl,token)

    logging.info("Processing basic info: username=%s", username)

    basic_info = _get_basic(username, gl)
    logging.info("Basic info: %s", basic_info)

    if not basic_info["id"]:
        raise ValueError("Failed to get user id")

    user_id = basic_info["id"]
    user_email = basic_info["email"]

    logging.info("Processing repos for user_id=%s", user_id)
    logging.info("Processing contributions for user=%s", username)

    repo_info,contribution_info = _get_repo(username,user_email,user_id, gl, year)

    return {
        "basic": basic_info,
        "repo": repo_info,
        "contribution": contribution_info,

    }

