from log.logging_config import setup_logging

import requests
from datetime import datetime
import urllib.parse
import pytz
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import time


setup_logging()


def _parse_time(time, timezone):
    result = None
    try:
        result = (
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
            .replace(tzinfo=pytz.UTC)
            .astimezone(timezone)
            .isoformat()
        )
    except Exception as e:
        logging.error(f"Failed to parse time: {e}")
        logging.error(f"Time: {time}")
        result = datetime(2000, 1, 1).isoformat()
    finally:
        return result


def _paginate(func: callable) -> callable:
    def wrapper(username, url, token, timezone, year):
        results = []
        while url:
            data, res, cont = func(username, url, token, timezone, year)
            if data:
                results.extend(data)
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
    url,
    token,
    per_page = 100,
    accept = "application/vnd.github.v3+json",
):
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

        logging.info(f"Fetching data from {url}...")

        response = requests.get(url, headers=headers)
        if response.status_code == 409:  # Empty repository
            return response

        response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to fetch data from {url}: {e}")
        logging.error(f"Response: {response}")
        raise e
    else:
        return response
    finally:
        time.sleep(0.3)


def get_github_info(username, token, timezone, year):
    user_url = f"https://api.github.com/users/{username}"
    response = _get_response(user_url, token)
    data = response.json()

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

    repos_url = f"https://api.github.com/user/repos"
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
    username, issues_url, token, timezone, year
):
    do_continue = True

    response = _get_response(issues_url, token)
    if response.status_code == 409:
        return [], response
    issues = response.json().get("items")

    issues_details = []

    for issue in issues:
        created_time = _parse_time(issue.get("created_at"), timezone)
        if datetime.fromisoformat(created_time).year < year:
            do_continue = False
        issues_details.append(
            {
                "url": issue.get("html_url"),
                "title": issue.get("title"),
                "body": issue.get("body"),
                "state": issue.get("state"),
                "created_time": created_time,
            }
        )

    return issues_details, response, do_continue


@_paginate
def _get_user_prs(
    username, prs_url, token, timezone, year
):
    do_continue = True

    response = _get_response(prs_url, token)
    if response.status_code == 409:
        return [], response
    prs = response.json().get("items")

    prs_details = []

    for pr in prs:
        created_time = _parse_time(pr.get("created_at"), timezone)
        if datetime.fromisoformat(created_time).year < year:
            do_continue = False

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

    return prs_details, response, do_continue


@_paginate
def _get_user_repos(
    username, repos_url, token, timezone, year
):
    response = _get_response(repos_url, token)
    if response.status_code == 409:
        return [], response
    repos = response.json()

    repos_details = []

    for repo in repos:
        try:
            if repo.get("fork"):
                continue

            language_url = repo.get("languages_url")
            languages_details = _get_user_repo_languages(
                language_url, token=token
            )

            commits_url = repo.get("commits_url").replace("{/sha}", "")
            commits_details = _get_user_commits(
                username=username, url=commits_url, token=token, timezone=timezone, year=year
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
        except Exception as e:
            logging.error(f"Failed to fetch repo: {e}")
            pass

    return repos_details, response, True


def _get_user_repo_languages(
    language_url, token
):
    response = _get_response(language_url, token)
    response.raise_for_status()
    languages_details = response.json()

    return languages_details


@_paginate
def _get_user_commits(
    username, commits_url, token, timezone, year
):
    do_continue = True

    response = _get_response(commits_url, token)
    if response.status_code == 409:
        return [], response
    response.raise_for_status()
    commits = response.json()

    commits_details = []

    for commit in commits:
        committer = None
        try:
            committer = commit.get("committer").get("login")
        except:
            committer = commit.get("commit").get("committer").get("name")
        if committer == username:
            commit_message = commit.get("commit").get("message")

            commit_time = _parse_time(
                commit.get("commit").get("committer").get("date"), timezone
            )
            if datetime.fromisoformat(commit_time).year < year:
                do_continue = False

            commits_details.append(
                {
                    "message": commit_message,
                    "created_time": commit_time,
                }
            )

    return commits_details, response, do_continue
