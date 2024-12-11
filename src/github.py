from datetime import datetime
import re

from src.basic import load_token, get_github_info
import src.filter as filter


class Github:
    def __init__(self, access_token: str, username: str):
        self.ACCESS_TOKEN = access_token
        self.USERNAME = username
        self.data = None

    def fetch_data(self):
        load_token(self.ACCESS_TOKEN)
        self.data = get_github_info(self.USERNAME)

        return self

    def count_repos_number(self):
        repos_number = len(self.data["repos_details"])
        self.data["repos_number"] = repos_number

        return self

    def filter_commits(self, year: int):
        self.data = filter.commits(self.data, year)

        return self

    def filter_repos(self, year: int):
        self.data = filter.repos(self.data, year)

        return self

    def filter_issues(self, year: int):
        self.data = filter.issues(self.data, year)

        return self

    def filter_prs(self, year: int):
        self.data = filter.prs(self.data, year)

        return self

    def filter_stars(self, year: int):
        self.data = filter.stars(self.data, year)

        return self

    def filter_all(self, year: int):
        self.filter_commits(year) \
            .filter_repos(year) \
            .filter_issues(year) \
            .filter_prs(year) \
            .filter_stars(year)

        return self

    def count_commits_types(self):
        commits_types = {}
        for repo in self.data["repos_details"]:
            repo_commits_types = {}
            for commit in repo["commits_details"]:
                commit_type = self.get_commits_type(commit["message"])

                if commit_type in repo_commits_types:
                    repo_commits_types[commit_type] += 1
                else:
                    repo_commits_types[commit_type] = 1

            repo["commits_types"] = repo_commits_types

            for key, value in repo_commits_types.items():
                if key in commits_types:
                    commits_types[key] += value
                else:
                    commits_types[key] = value

        self.data["commits_types"] = commits_types

        return self

    def count_commits_number(self):
        commits_number = 0
        for repo in self.data["repos_details"]:
            repo["commits_number"] = len(repo["commits_details"])
            commits_number += len(repo["commits_details"])

        self.data["commits_number"] = commits_number

        return self

    def sort_commits(self):
        for repo in self.data["repos_details"]:
            repo["commits_details"] = sorted(
                repo["commits_details"],
                key=lambda x: datetime.fromisoformat(x["time"]),
                reverse=True,
            )

        return self

    def count_repos_languages(self):
        repos_languages = {}
        for repo in self.data["repos_details"]:
            for key, value in repo["languages_details"].items():
                if key in repos_languages:
                    repos_languages[key] += value
                else:
                    repos_languages[key] = value

            repo["languages_details"] = dict(
                sorted(
                    repo["languages_details"].items(), key=lambda x: x[1], reverse=True
                )
            )

        self.data["repos_languages"] = repos_languages
        self.data["repos_languages"] = dict(
            sorted(
                self.data["repos_languages"].items(), key=lambda x: x[1], reverse=True
            )
        )

        return self

    def count_repos_stargazer(self):
        stargazers_count = 0
        for repo in self.data["repos_details"]:
            stargazers_count += repo["stargazers_count"]

        self.data["stargazers_count"] = stargazers_count

        return self

    def count_repos_forks(self):
        forks_count = 0
        for repo in self.data["repos_details"]:
            forks_count += repo["forks_count"]

        self.data["forks_count"] = forks_count

        return self

    def count_repos_number(self):
        repos_number = len(self.data["repos_details"])
        self.data["repos_number"] = repos_number

        return self

    def sort_repos(self):
        self.data["repos_details"] = sorted(
            self.data["repos_details"],
            key=lambda x: datetime.fromisoformat(x["created_at"]),
            reverse=True,
        )

        return self

    def sort_repos_by_stargazers(self):
        self.data["repos_details"] = sorted(
            self.data["repos_details"],
            key=lambda x: x["stargazers_count"],
            reverse=True,
        )

        return self

    def count_issues_number(self):
        issues_number = len(self.data["issues_details"])
        self.data["issues_number"] = issues_number

        return self

    def sort_issues(self):
        self.data["issues_details"] = sorted(
            self.data["issues_details"],
            key=lambda x: datetime.fromisoformat(x["created_time"]),
            reverse=True,
        )

        return self

    def count_prs_number(self):
        prs_number = len(self.data["prs_details"])
        self.data["prs_number"] = prs_number

        return self

    def count_merged_prs_number(self):
        merged_prs_number = len(
            list(filter(lambda x: x["merged"], self.data["prs_details"]))
        )
        self.data["merged_prs_number"] = merged_prs_number

        return self

    def sort_prs(self):
        self.data["prs_details"] = sorted(
            self.data["prs_details"],
            key=lambda x: datetime.fromisoformat(x["created_time"]),
            reverse=True,
        )

        return self

    def count_stars_number(self):
        stars_number = len(self.data["stars_details"])
        self.data["stars_number"] = stars_number

        return self

    def sort_stars(self):
        self.data["stars_details"] = sorted(
            self.data["stars_details"],
            key=lambda x: datetime.fromisoformat(x["starred_time"]),
            reverse=True,
        )

        return self

    def count_all(self):
        self.count_repos_number().count_issues_number().count_prs_number().count_merged_prs_number().count_stars_number().count_commits_number().count_commits_types().count_repos_languages().count_repos_stargazer().count_repos_forks()

        return self

    def sort_all(self):
        self.sort_repos().sort_issues().sort_prs().sort_stars().sort_commits()

        return self

    @property
    def result(self):
        return self.data

    @result.setter
    def result(self, value):
        self.data = value

    @staticmethod
    def get_commits_type(message: str) -> str:
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
