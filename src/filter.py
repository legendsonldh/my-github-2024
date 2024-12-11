from datetime import datetime

def _filter(data, key: str, year: int):
    return list(filter(lambda x: datetime.fromisoformat(x[key]).year == year, data))


def commits(data, year: int):
    for repo in data["repos_details"]:
        repo["commits_details"] = _filter(repo["commits_details"], "time", year)

    data["repos_details"] = list(filter(lambda x: len(x["commits_details"]) > 0, data["repos_details"]))

    return data


def repos(data, year: int):
    data["repos_details"] = _filter(data["repos_details"], "created_at", year)

    return data


def issues(data, year: int):
    data["issues_details"] = _filter(data["issues_details"], "created_time", year)

    return data


def prs(data, year: int):
    data["prs_details"] = _filter(data["prs_details"], "created_time", year)

    return data


def stars(data, year: int):
    data["stars_details"] = _filter(data["stars_details"], "starred_time", year)

    return data
