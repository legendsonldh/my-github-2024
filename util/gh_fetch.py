"""
This module fetches the Github user information.

Functions:
    get_github_info(username: str, token: str, timezone: pytz.timezone, year: int) -> dict:
        Get the Github user information.

    _get_response(url: str, token: str, per_page: int = 100, accept: str = 
                  "application/vnd.github.v3+json", timeout: int = 10) -> requests.Response:
        Get the response from the Github API.

    _parse_time(time_str: str, timezone: pytz.timezone) -> str:
        Parse the time string to the timezone.

    _paginate(func: callable) -> callable:
        Paginate the data from the Github API.

    _get_user_issues(username: str, url: str, token: str, timezone: pytz.timezone, 
                     year: int) -> list:
        Get the user issues.

    _get_user_prs(username: str, url: str, token: str, timezone: pytz.timezone, 
                  year: int) -> list:
        Get the user pull requests.

    _get_user_repos(username: str, url: str, token: str, timezone: pytz.timezone, 
                    year: int) -> list:
        Get the user repositories.

    _get_user_repo_languages(url: str, token: str) -> dict:
        Get the user repository languages.

    _get_user_commits(username: str, url: str, token: str, timezone: pytz.timezone, 
                      year: int) -> list:
        Get the user commits.
"""

import logging
import time
import urllib.parse
from datetime import datetime

import pytz
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from log.logging_config import setup_logging

setup_logging()


def _parse_time(time_str: str, timezone: pytz.timezone) -> str:
    """
    Parse the time string to the timezone.

    Args:
        time_str (str): The time string.
        timezone (pytz.timezone): The timezone.

    Returns:
        str: The time string in the timezone.
    """
    result = None
    try:
        result = (
            datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
            .replace(tzinfo=pytz.UTC)
            .astimezone(timezone)
            .isoformat()
        )
    except ValueError as e:
        logging.error("Failed to parse time: %s", e)
        logging.error("Time: %s", time_str)
        result = datetime(2000, 1, 1).isoformat()
    except pytz.UnknownTimeZoneError as e:
        logging.error("Unknown timezone: %s", e)
        result = datetime(2000, 1, 1).isoformat()

    return result


def _paginate(func: callable) -> callable:
    """
    Paginate the data from the Github API.

    Args:
        func (callable): The function to paginate.

    Returns:
        callable: The wrapper function to paginate the data.
    """

    def wrapper(
        username: str, url: str, token: str, timezone: pytz.timezone, year: int
    ) -> list:
        """
        Wrapper function to paginate the data.

        Args:
            username (str): The Github username.
            url (str): The Github API URL to fetch the data.
            token (str): The Github access token.
            timezone (pytz.timezone): The timezone.
            year (int): The year to fetch the data.

        Returns:
            list: The paginated results.
        """
        results = []

        while url:
            data, res, cont = func(username, url, token, timezone, year)
            if data:
                results.extend(data)

            logging.info("Total %d items fetched, continue: %s", len(results), cont)

            if len(results) > 10000:
                return results

            links = res.headers.get("Link")

            if links and cont:
                next_url = None
                for link in links.split(","):
                    if 'rel="next"' in link:
                        next_url = link[link.find("<") + 1 : link.find(">")]
                        break
                url = next_url
            else:
                url = None
        return results

    return wrapper


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _get_response(
    url: str,
    token: str,
    per_page: int = 100,
    accept: str = "application/vnd.github.v3+json",
    timeout: int = 10,  # Default timeout is 10 seconds
) -> requests.Response:
    """
    Get the response from the Github API.

    Args:
        url (str): The Github API URL to fetch the data.
        token (str): The Github access token.
        per_page (int): The number of items per page.
        accept (str): The accept header.
        timeout (int): The timeout for the request in seconds.

    Returns:
        requests.Response: The response from the Github API.
    """
    response = None
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": accept,
        }

        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        query_params["per_page"] = str(per_page)
        new_query_string = urllib.parse.urlencode(query_params, doseq=True)
        url = urllib.parse.urlunparse(parsed_url._replace(query=new_query_string))

        logging.info("Fetching data from %s", url)

        response = requests.get(
            url, headers=headers, timeout=timeout
        )  # Adding the timeout argument
        if response.status_code == 409:  # Empty repository
            return response

        response.raise_for_status()
    except Exception as e:
        logging.error("Failed to fetch data from %s: %s", url, e)
        logging.error("Response: %s", response.text)
        raise e
    else:
        return response
    finally:
        time.sleep(0.3)


def get_github_info(
    username: str, token: str, timezone: pytz.timezone, year: int
) -> dict:
    """
    Get the Github user information.

    Args:
        username (str): The Github username.
        token (str): The Github access token.
        timezone (pytz.timezone): The timezone.
        year (int): The year to fetch the data.

    Returns:
        dict: The Github user information.
    """
    user_url = f"https://api.github.com/users/{username}"
    response = _get_response(user_url, token)
    data = response.json()

    year = int(year)

    created_time = (
        datetime.now() - datetime.strptime(data.get("created_at"), "%Y-%m-%dT%H:%M:%SZ")
    ).days

    isssues_url = f"https://api.github.com/search/issues?q=author:{username}+type:issue"
    issues_details = _get_user_issues(
        username=username, url=isssues_url, token=token, timezone=timezone, year=year
    )

    prs_url = f"https://api.github.com/search/issues?q=author:{username}+type:pr"
    prs_details = _get_user_prs(
        username=username, url=prs_url, token=token, timezone=timezone, year=year
    )

    repos_url = "https://api.github.com/user/repos"
    repos_details = _get_user_repos(
        username=username, url=repos_url, token=token, timezone=timezone, year=year
    )

    return {
        "account_info": {
            "url": data.get("html_url"),
            "name": data.get("name"),
            "username": data.get("login"),
            "avatar": data.get("avatar_url"),
            "bio": data.get("bio"),
            "followers_num": data.get("followers"),
            "following_num": data.get("following"),
            "created_time": created_time,
        },
        "issues_details": issues_details,
        "prs_details": prs_details,
        "repos_details": repos_details,
    }


@_paginate
def _get_user_issues(
    username: str, url: str, token: str, timezone: pytz.timezone, year: int
) -> list:
    """
    Get the user issues.

    Args:
        username (str): The Github username.
        url (str): The Github API URL.
        token (str): The Github access token.
        timezone (pytz.timezone): The timezone.
        year (int): The year to fetch the data.

    Returns:
        list: The user issues.
    """

    _ = username  # Avoid pylint error

    response = _get_response(url, token)
    if response.status_code == 409:
        return [], response
    issues = response.json().get("items")

    issues_details = []

    for issue in issues:
        created_time = _parse_time(issue.get("created_at"), timezone)
        if datetime.fromisoformat(created_time).year < year:
            return issues_details, response, False

        issues_details.append(
            {
                "url": issue.get("html_url"),
                "title": issue.get("title"),
                "body": issue.get("body"),
                "state": issue.get("state"),
                "created_time": created_time,
            }
        )

    return issues_details, response, True


@_paginate
def _get_user_prs(
    username: str, url: str, token: str, timezone: pytz.timezone, year: int
) -> list:
    """
    Get the user pull requests.

    Args:
        username (str): The Github username.
        url (str): The Github API URL.
        token (str): The Github access token.
        timezone (pytz.timezone): The timezone.
        year (int): The year to fetch the data.

    Returns:
        list: The user pull requests.
    """
    _ = username  # Avoid pylint error

    response = _get_response(url, token)
    if response.status_code == 409:
        return [], response
    prs = response.json().get("items")

    prs_details = []

    for pr in prs:
        created_time = _parse_time(pr.get("created_at"), timezone)
        if datetime.fromisoformat(created_time).year < year:
            return prs_details, response, False

        if pr.get("pull_request").get("merged_at"):
            merged = True
            merged_time = _parse_time(pr.get("pull_request").get("merged_at"), timezone)
        else:
            merged = False
            merged_time = None

        prs_details.append(
            {
                "url": pr.get("html_url"),
                "title": pr.get("title"),
                "body": pr.get("body"),
                "state": pr.get("state"),
                "created_time": created_time,
                "merged": merged,
                "merged_time": merged_time,
            }
        )

    return prs_details, response, True


@_paginate
def _get_user_repos(
    username: str, url: str, token: str, timezone: pytz.timezone, year: int
) -> list:
    """
    Get the user repositories.

    Args:
        username (str): The Github username.
        url (str): The Github API URL.
        token (str): The Github access token.
        timezone (pytz.timezone): The timezone.
        year (int): The year to fetch the data.

    Returns:
        list: The user repositories.
    """
    response = _get_response(url, token)
    if response.status_code == 409:
        return [], response
    repos = response.json()

    repos_details = []

    for repo in repos:
        try:
            language_url = repo.get("languages_url")
            languages_details = _get_user_repo_languages(language_url, token=token)

            commits_url = repo.get("commits_url").replace("{/sha}", "")
            commits_details = _get_user_commits(
                username=username,
                url=commits_url,
                token=token,
                timezone=timezone,
                year=year,
            )

            repos_details.append(
                {
                    "url": repo.get("html_url"),
                    "name": repo.get("name"),
                    "description": repo.get("description"),
                    "created_time": repo.get("created_at"),
                    "stargazers_num": repo.get("stargazers_count"),
                    "forks_num": repo.get("forks_count"),
                    "languages_num": languages_details,
                    "commits_details": commits_details,
                }
            )
        except requests.exceptions.RequestException as e:
            logging.error("Request failed: %s", e)
        except KeyError as e:
            logging.error("Key error: %s", e)
        except (TypeError, ValueError) as e:
            logging.error("Type or Value error: %s", e)

    return repos_details, response, True


def _get_user_repo_languages(url: str, token: str) -> dict:
    """
    Get the user repository languages.

    Args:
        url (str): The Github API URL.
        token (str): The Github access token.

    Returns:
        dict: The user repository languages.
    """
    response = _get_response(url, token)
    response.raise_for_status()
    languages_details = response.json()

    return languages_details


@_paginate
def _get_user_commits(
    username: str, url: str, token: str, timezone: pytz.timezone, year: int
) -> list:
    """
    Get the user commits.

    Args:
        username (str): The Github username.
        url (str): The Github API URL.
        token (str): The Github access token.
        timezone (pytz.timezone): The timezone.
        year (int): The year to fetch the data.

    Returns:
        list: The user commits.
    """
    response = _get_response(url, token)
    if response.status_code == 409:
        return [], response
    response.raise_for_status()
    commits = response.json()

    commits_details = []

    for commit in commits:
        committer = None
        try:
            committer = commit.get("committer").get("login")
        except AttributeError:
            committer = commit.get("commit").get("committer").get("name")
        if committer == username:
            commit_message = commit.get("commit").get("message")

            commit_time = _parse_time(
                commit.get("commit").get("committer").get("date"), timezone
            )
            if datetime.fromisoformat(commit_time).year < year:
                return commits_details, response, False

            commits_details.append(
                {
                    "message": commit_message,
                    "created_time": commit_time,
                }
            )

    return commits_details, response, True
