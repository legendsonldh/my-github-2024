"""
This module provides functions to sort GitHub repository data.

Functions:
    commits_time(data: dict) -> dict:
        Sorts the commits by their creation time in descending order.

    repos_time(data: dict) -> dict:
        Sorts the repositories by their creation time in descending order.

    repos_stargazer(data: dict) -> dict:
        Sorts the repositories by the number of stargazers in descending order.

    issues_time(data: dict) -> dict:
        Sorts the issues by their creation time in descending order.

    prs_time(data: dict) -> dict:
        Sorts the pull requests by their creation time in descending order.
"""

from datetime import datetime


def commits_time(data: dict) -> dict:
    """
    Sort the commits by time.

    Args:
        data (dict): The data to sort.

    Returns:
        dict: The sorted data.
    """
    for repo in data["repos_details"]:
        repo["commits_details"] = sorted(
            repo["commits_details"],
            key=lambda x: datetime.fromisoformat(x["created_time"]),
            reverse=True,
        )

    return data


def repos_time(data: dict) -> dict:
    """
    Sort the repos by time.

    Args:
        data (dict): The data to sort.

    Returns:
        dict: The sorted data.
    """
    data["repos_details"] = sorted(
        data["repos_details"],
        key=lambda x: datetime.fromisoformat(x["created_time"]),
        reverse=True,
    )

    return data


def repos_stargazer(data: dict) -> dict:
    """
    Sort the repos by stargazer.

    Args:
        data (dict): The data to sort.

    Returns:
        dict: The sorted data.
    """
    data["repos_details"] = sorted(
        data["repos_details"],
        key=lambda x: x["stargazers_num"],
        reverse=True,
    )

    return data


def issues_time(data: dict) -> dict:
    """
    Sort the issues by time.

    Args:
        data (dict): The data to sort.

    Returns:
        dict: The sorted data.
    """
    data["issues_details"] = sorted(
        data["issues_details"],
        key=lambda x: datetime.fromisoformat(x["created_time"]),
        reverse=True,
    )

    return data


def prs_time(data: dict) -> dict:
    """
    Sort the PRs by time.

    Args:
        data (dict): The data to sort.

    Returns:
        dict: The sorted data.
    """
    data["prs_details"] = sorted(
        data["prs_details"],
        key=lambda x: datetime.fromisoformat(x["created_time"]),
        reverse=True,
    )

    return data
