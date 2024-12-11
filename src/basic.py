import requests
from datetime import datetime
import os
import re
import json
from typing import Dict, List, Tuple, Any
from dotenv import load_dotenv
import urllib.parse

URL = str
JSON = Dict[str, Any] | List[Dict[str, Any]]

def load_token(token: str):
    global ACCESS_TOKEN
    ACCESS_TOKEN = token

def paginate(func: callable) -> callable:
    def wrapper(username: str, url: URL) -> JSON:
        results = []
        while url:
            data, res = func(username, url)
            if data:
                results.extend(data)
            links = res.headers.get("Link")
            if links:
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

def get_response(url: URL, per_page: int = 100, accept: str = "application/vnd.github.v3+json") -> requests.Response:
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": accept,
    }

    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    query_params["per_page"] = str(per_page)
    new_query_string = urllib.parse.urlencode(query_params, doseq=True)
    url = urllib.parse.urlunparse(parsed_url._replace(query=new_query_string))

    print(f"Fetching data from {url}...")
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response

def get_github_info(username: str) -> JSON:
    user_url = f"https://api.github.com/users/{username}"
    response = get_response(user_url)
    data = response.json()

    created_time = (
        datetime.now() - datetime.strptime(data.get("created_at"), "%Y-%m-%dT%H:%M:%SZ")
    ).days

    isssues_url = f"https://api.github.com/search/issues?q=author:{username}+type:issue"
    issues_details = get_user_issues(username=username, url=isssues_url)

    prs_url = f"https://api.github.com/search/issues?q=author:{username}+type:pr"
    prs_details = get_user_prs(username=username, url=prs_url)

    repos_url = data.get("repos_url")
    repos_details = get_user_repos(username=username, url=repos_url)

    stars_url = data.get("starred_url").replace("{/owner}{/repo}", "")
    stars_details = get_user_stars(username=username, url=stars_url)

    return {
        "html_url": data.get("html_url"),
        "name": data.get("name"),
        "username": data.get("login"),
        "avatar_url": data.get("avatar_url"),
        "bio": data.get("bio"),
        "public_repos_num": data.get("public_repos"),
        # "public_gists_num": data.get("public_gists"),
        "followers_num": data.get("followers"),
        "following_num": data.get("following"),
        "created_time": created_time,
        "issues_details": issues_details,
        "prs_details": prs_details,
        "repos_details": repos_details,
        "stars_details": stars_details,
    }


@paginate
def get_user_issues(username: str, issues_url: URL) -> Tuple[JSON, requests.Response]:
    response = get_response(issues_url)
    issues = response.json().get("items")

    issues_details = []

    for issue in issues:
        created_time = datetime.strptime(
            issue.get("created_at"), "%Y-%m-%dT%H:%M:%SZ"
        ).isoformat()

        issues_details.append(
            {
                "html_url": issue.get("html_url"),
                "title": issue.get("title"),
                "body": issue.get("body"),
                "state": issue.get("state"),
                "created_time": created_time,
            }
        )

    return issues_details, response


@paginate
def get_user_prs(username: str, prs_url: URL) -> Tuple[JSON, requests.Response]:
    response = get_response(prs_url)
    prs = response.json().get("items")

    prs_details = []

    for pr in prs:
        created_time = datetime.strptime(
            pr.get("created_at"), "%Y-%m-%dT%H:%M:%SZ"
        ).isoformat()
        
        if pr.get("pull_request").get("merged_at"):
            merged = True
            merged_time = datetime.strptime(
                pr.get("pull_request").get("merged_at"), "%Y-%m-%dT%H:%M:%SZ"
            ).isoformat()
        else:
            merged = False
            merged_time = None

        prs_details.append(
            {
                "html_url": pr.get("html_url"),
                "title": pr.get("title"),
                "body": pr.get("body"),
                "state": pr.get("state"),
                "created_time": created_time,
                "merged": merged,
                "merged_time": merged_time,
            }
        )

    return prs_details, response


@paginate
def get_user_stars(username: str, stars_url: URL) -> Tuple[JSON, requests.Response]:
    response = get_response(stars_url, accept="application/vnd.github.v3.star+json")
    stars = response.json()

    stars_details = []

    for star in stars:
        starred_time = datetime.strptime(
            star.get("starred_at"), "%Y-%m-%dT%H:%M:%SZ"
        ).isoformat()

        stars_details.append(
            {
                "html_url": star.get("repo").get("html_url"),
                "name": star.get("repo").get("full_name"),
                "starred_time": starred_time,
            }
        )

    return stars_details, response


@paginate
def get_user_repos(username: str, repos_url: URL) -> Tuple[JSON, requests.Response]:
    response = get_response(repos_url)
    repos = response.json()

    repos_details = []

    for repo in repos:
        if repo.get("fork"):
            continue

        language_url = repo.get("languages_url")
        languages_details = get_user_repo_languages(language_url)

        commits_url = repo.get("commits_url").replace("{/sha}", "")
        commits_details = get_user_commits(username=username, url=commits_url)

        repos_details.append(
            {
                "html_url": repo.get("html_url"),
                "name": repo.get("name"),
                "description": repo.get("description"),
                "created_at": repo.get("created_at"),
                "stargazers_count": repo.get("stargazers_count"),
                "forks_count": repo.get("forks_count"),
                "languages_details": languages_details,
                "commits_details": commits_details,
            }
        )

    return repos_details, response


def get_user_repo_languages(language_url: URL) -> JSON:
    response = get_response(language_url)
    response.raise_for_status()
    languages_details = response.json()

    return languages_details

@paginate
def get_user_commits(username: str, commits_url: URL) -> Tuple[JSON, requests.Response]:
    response = get_response(commits_url)
    response.raise_for_status()
    commits = response.json()

    commits_details = []

    for commit in commits:
        # print(json.dumps(commit, indent=4))
        committer = None
        try:
            committer = commit.get("committer").get("login")
        except:
            committer = commit.get("commit").get("committer").get("name")
        if committer == username:
            commit_message = commit.get("commit").get("message")

            commit_time = datetime.strptime(
                commit.get("commit").get("committer").get("date"),
                "%Y-%m-%dT%H:%M:%SZ",
            ).isoformat()

            commits_details.append(
                {
                    "message": commit_message,
                    "time": commit_time,
                }
            )

    return commits_details, response

if __name__ == "__main__":
    username = "WCY-dt"

    try:
        username = "WCY-dt"
        result = get_github_info(username)
        # print(json.dumps(result, indent=4))
        with open("info.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result, indent=4))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print("Fetched successfully!")
