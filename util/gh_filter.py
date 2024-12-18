"""
This module contains functions to filter the data by a specific year or a key in the JSON format.

Functions:
    commits_year(data: dict, year: int) -> dict:
        Filters the commits in the data by a specific year.

    repos_year(data: dict, year: int) -> dict:
        Filters the repositories in the data by a specific year.

    issues_year(data: dict, year: int) -> dict:
        Filters the issues in the data by a specific year.

    prs_year(data: dict, year: int) -> dict:
        Filters the pull requests in the data by a specific year.

    json_key(data: dict, key: dict) -> dict:
        Filter the data by a key in the JSON format.
"""

from datetime import datetime


def _filter_year(data: list, key: str, year: int) -> list:
    """
    Filters a list of dictionaries by a specific year.

    Args:
        data (list): The list of dictionaries to filter.
        key (str): The key in the dictionary to check the date.
        year (int): The year to filter by.

    Returns:
        list: The filtered list of dictionaries.
    """
    return list(filter(lambda x: datetime.fromisoformat(x[key]).year == year, data))


def commits_year(data: dict, year: int) -> dict:
    """
    Filters the commits in the data by a specific year.

    Args:
        data (dict): The data containing repository details.
        year (int): The year to filter by.

    Returns:
        dict: The data with filtered commits.
    """
    for repo in data["repos_details"]:
        repo["commits_details"] = _filter_year(
            repo["commits_details"], "created_time", year
        )

    data["repos_details"] = list(
        filter(lambda x: len(x["commits_details"]) > 0, data["repos_details"])
    )

    return data


def repos_year(data: dict, year: int) -> dict:
    """
    Filters the repositories in the data by a specific year.

    Args:
        data (dict): The data containing repository details.
        year (int): The year to filter by.

    Returns:
        dict: The data with filtered repositories.
    """
    data["repos_details"] = _filter_year(data["repos_details"], "created_time", year)

    return data


def issues_year(data: dict, year: int) -> dict:
    """
    Filters the issues in the data by a specific year.

    Args:
        data (dict): The data containing repository details.
        year (int): The year to filter by.

    Returns:
        dict: The data with filtered issues.
    """
    data["issues_details"] = _filter_year(data["issues_details"], "created_time", year)

    return data


def prs_year(data: dict, year: int) -> dict:
    """
    Filters the pull requests in the data by a specific year.

    Args:
        data (dict): The data containing repository details.
        year (int): The year to filter by.

    Returns:
        dict: The data with filtered pull requests.
    """
    data["prs_details"] = _filter_year(data["prs_details"], "created_time", year)

    return data


def json_key(data: dict, key: dict) -> dict:
    """
    Filter the data by a key in the JSON format.

    Args:
        data (dict): The data to filter.
        key (dict): The key to filter the data.

    Returns:
        dict: The filtered data.
    """
    if isinstance(data, list):
        return [json_key(x, key) for x in data]

    json_key_result = {}

    for k, v in key.items():
        if k not in data:
            raise KeyError(f"KeyError: {k} not found in {data}")

        if isinstance(v, dict):
            json_key_result[k] = json_key(data[k], v)
        else:
            json_key_result[k] = data[k]

    return json_key_result
