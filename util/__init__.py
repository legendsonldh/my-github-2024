"""
This module provides utilities for interacting with the Github API.

Classes:
    Github: A class for interacting with the Github API, including methods for fetching,
            filtering, counting, sorting, reading, and writing data.
"""

import json
import logging
from datetime import timedelta
from datetime import timezone as dt_timezone
from typing import Any

import pytz

from log.logging_config import setup_logging
from util import gh_count, gh_filter, gh_sort
from util.gh_fetch import get_github_info

setup_logging()


class Github:
    """
    The Github class for interacting with the Github API.

    Attributes:
        access_token (str): The Github access token.
        username (str): The Github username.
        timezone (pytz.BaseTzInfo): The timezone.
        data (dict | list | None): The fetched data.

    Methods:
        _parse_timezone: Parse the timezone string to a pytz timezone object.
        fetch_data: Fetch the data from the Github API.
        filter_data: Filter the filter type data by the year.
        count_data: Count the count type data.
        sort_data: Sort the sort type data by the sort by.
        filter_all: Filter commits, issues, and prs data by the year.
        filter_repos: Filter repos data by the year.
        filter_json: Filter the data by a key in the JSON format.
        count_all: Count all the data including commits, commits types, commits monthly,
                   commits weekdaily, commits daily, commits hourly, repos, repos languages,
                   repos stargazer, repos fork, prs, prs merged, and issues.
        sort_all: Sort all the data including commits by time, repos by time, repos by stargazer,
                  prs by time, and issues by time.
        read_from_file: Read the data from a file.
        write_to_file: Write the data to a file.
        _get_result_structure: Get the result structure of the data.
        print_result_structure: Print the result structure of the data.
        result: Get the result data.

    Properties:
        result: Get the result data.
    """

    data: dict[str, Any] | None

    def __init__(
        self, access_token: str, username: str, timezone: str = "Asia/Shanghai"
    ) -> None:
        """
        Initialize the Github object with the access token, username, and timezone.

        Args:
            access_token (str): The Github access token.
            username (str): The Github username.
            timezone (str): The timezone string.
        """
        self.access_token: str = access_token
        self.username: str = username
        self.timezone: pytz.BaseTzInfo = self._parse_timezone(timezone)
        self.data = None

    def _parse_timezone(self, tz_str: str) -> pytz.BaseTzInfo:
        """
        Parse the timezone string to a pytz timezone object.

        Args:
            tz_str (str): The timezone string.

        Returns:
            pytz.BaseTzInfo: The pytz timezone object.
        """
        try:
            return pytz.timezone(tz_str)
        except pytz.UnknownTimeZoneError as e:
            if tz_str.startswith("+") or tz_str.startswith("-"):
                hours_offset = int(tz_str)
                timezone = dt_timezone(timedelta(hours=hours_offset))
                return pytz.timezone(str(timezone))

            raise e

    def fetch_data(self, year: int) -> "Github":
        """
        Fetch the data from the Github API.

        Args:
            year (int): The year to fetch the data.

        Returns:
            Github: The Github object with the fetched data.
        """
        self.data = get_github_info(
            self.username, self.access_token, self.timezone, year
        )
        return self

    def filter_data(self, filter_type: str, year: int) -> "Github":
        """
        Filter the filter type data by the year.

        Args:
            filter_type (str): The data to filter.
            year (int): The year to filter the data.

        Returns:
            Github: The Github object with the filtered data.
        """
        filter_func = getattr(gh_filter, f"{filter_type}_year")
        self.data = filter_func(self.data, year)
        return self

    def count_data(self, count_type: str) -> "Github":
        """
        Count the count type data.

        Args:
            count_type (str): The data to count.

        Returns:
            Github: The Github object with the counted data.
        """
        count_func = getattr(gh_count, f"{count_type}_number")
        self.data = count_func(self.data)
        return self

    def sort_data(self, sort_type: str, sort_by: str) -> "Github":
        """
        Sort the sort type data by the sort by.

        Args:
            sort_type (str): The data to sort.
            sort_by (str): The key to sort by.

        Returns:
            Github: The Github object with the sorted data.
        """
        sort_func = getattr(gh_sort, f"{sort_type}_{sort_by}")
        self.data = sort_func(self.data)
        return self

    def filter_all(self, year: int) -> "Github":
        """
        Filter commits, issues, and prs data by the year.

        Args:
            year (int): The year to filter the data.

        Returns:
            Github: The Github object with the filtered data.
        """
        for filter_type in ["commits", "issues", "prs"]:
            self.filter_data(filter_type, year)
        return self

    def filter_repos(self, year: int) -> "Github":
        """
        Filter repos data by the year.

        Args:
            year (int): The year to filter the data.

        Returns:
            Github: The Github object with the filtered data.
        """
        self.filter_data("repos", year)
        return self

    def filter_json(self, key: dict) -> "Github":
        """
        Filter the data by a key in the JSON format.

        Args:
            key (dict): The key to filter the data.

        Returns:
            Github: The Github object with the filtered data.
        """
        if self.data is not None:
            self.data = gh_filter.json_key(self.data, key)
        return self

    def count_all(self) -> "Github":
        """
        Count all the data including commits, commits types, commits monthly, commits weekdaily, 
        commits daily, commits hourly, repos, repos languages, repos stargazer, repos fork, prs, 
        prs merged, and issues.

        Returns:
            Github: The Github object with the counted data.
        """
        for count_type in [
            "commits",
            "commits_types",
            "commits_monthly",
            "commits_weekdaily",
            "commits_daily",
            "commits_hourly",
            "repos",
            "repos_languages",
            "repos_stargazer",
            "repos_fork",
            "prs",
            "prs_merged",
            "issues",
        ]:
            self.count_data(count_type)
        return self

    def sort_all(self) -> "Github":
        """
        Sort all the data including commits by time, repos by time, repos by stargazer, prs by 
        time, and issues by time.

        Returns:
            Github: The Github object with the sorted data.
        """
        for sort_type, sort_by in [
            ("commits", "time"),
            ("repos", "time"),
            ("repos", "stargazer"),
            ("prs", "time"),
            ("issues", "time"),
        ]:
            self.sort_data(sort_type, sort_by)
        return self

    def read_from_file(self, filename: str) -> "Github":
        """
        Read the data from a file.

        Args:
            filename (str): The filename to read the data from.

        Returns:
            Github: The Github object with the data read from the file.
        """
        with open(filename, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        return self

    def write_to_file(self, filename: str) -> "Github":
        """
        Write the data to a file.

        Args:
            filename (str): The filename to write the data to.

        Returns:
            Github: The Github object with the data written to the file.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.result, indent=4))
        return self

    def _get_result_structure(self, data: dict | list | None) -> dict | list | str:
        """
        Get the result structure of the data.

        Args:
            data (dict | list): The data to get the result structure from.

        Returns:
            dict | list | str: The result structure of the data.
        """
        if isinstance(data, list):
            return [self._get_result_structure(data[0])]
        if isinstance(data, dict):
            return {k: self._get_result_structure(v) for k, v in data.items()}
        return type(data).__name__

    def print_result_structure(self) -> "Github":
        """
        Print the result structure of the data.

        Returns:
            Github: The Github object.
        """
        logging.info("Result structure: %s", self._get_result_structure(self.result))
        return self

    @property
    def result(self) -> dict | list | None:
        """
        Get the result data.

        Returns:
            dict | list: The result data.
        """
        return self.data

    @result.setter
    def result(self, value: dict[str, Any] | None) -> None:
        """
        Set the result data.

        Args:
            value (dict | list): The result data.
        """
        self.data = value
