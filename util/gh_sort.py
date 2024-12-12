from datetime import datetime


def commits_time(data):
    for repo in data["repos_details"]:
        repo["commits_details"] = sorted(
            repo["commits_details"],
            key=lambda x: datetime.fromisoformat(x["created_time"]),
            reverse=True,
        )

    return data


def repos_time(data):
    data["repos_details"] = sorted(
        data["repos_details"],
        key=lambda x: datetime.fromisoformat(x["created_time"]),
        reverse=True,
    )

    return data


def repos_stargazer(data):
    data["repos_details"] = sorted(
        data["repos_details"],
        key=lambda x: x["stargazers_num"],
        reverse=True,
    )

    return data


def issues_time(data):
    data["issues_details"] = sorted(
        data["issues_details"],
        key=lambda x: datetime.fromisoformat(x["created_time"]),
        reverse=True,
    )

    return data


def prs_time(data):
    data["prs_details"] = sorted(
        data["prs_details"],
        key=lambda x: datetime.fromisoformat(x["created_time"]),
        reverse=True,
    )

    return data


def stars_time(data):
    data["stars_details"] = sorted(
        data["stars_details"],
        key=lambda x: datetime.fromisoformat(x["created_time"]),
        reverse=True,
    )

    return data
