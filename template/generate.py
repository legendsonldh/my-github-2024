import json
import shutil
import os

def generate_site(year: int):
    data = None
    with open("data/result.json", "r") as f:
        data = json.load(f)
    data_new_repo = None
    with open("data/result_new_repo.json", "r") as f:
        data_new_repo = json.load(f)

    commits_per_day = data["commits_daily_num"][str(year)]
    longest_streak = 0
    current_streak = 0
    longest_break = 0
    current_break = 0

    for commits in commits_per_day:
        if commits > 0:
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
        else:
            current_streak = 0

        if commits == 0:
            current_break += 1
            if current_break > longest_break:
                longest_break = current_break
        else:
            current_break = 0

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = [f"{i}:00" for i in range(24)]

    created_days = data["account_info"]["created_time"]
    created_days = (int(created_days) + 99) // 100 * 100

    context = {
        "YEAR": year,

        "USERNAME": data["account_info"]["username"],
        "NAME": data["account_info"]["name"],
        "CREATED_TIME": created_days,
        "FOLLOWERS_NUM": data["account_info"]["followers_num"],
        "FOLLOWING_NUM": data["account_info"]["following_num"],
        "STARS_NUM": data["stargazers_num"],

        "COMMITS_PER_DAY": commits_per_day,
        "COMMITS_DAYS_NUM": len([x for x in commits_per_day if x > 0]),
        "LONGEST_COMMIT_STREAK": longest_streak,
        "LONGEST_COMMIT_BREAK": longest_break,
        "MAX_COMMITS_PER_DAY": max(commits_per_day),

        "COMMITS_PER_MONTH": data["commits_monthly_num"],
        "MOST_ACTIVE_MONTH": months[data["commits_monthly_num"].index(max(data["commits_monthly_num"]))],
        "COMMITS_PER_WEEKDAY": data["commits_weekdaily_num"],
        "MOST_ACTIVE_WEEKDAY": weekdays[data["commits_weekdaily_num"].index(max(data["commits_weekdaily_num"]))],
        "COMMITS_PER_HOUR": data["commits_hourly_num"],
        "MOST_ACTIVE_HOUR": hours[data["commits_hourly_num"].index(max(data["commits_hourly_num"]))],

        "COMMITS_NUM": data["commits_num"],
        "ISSUES_NUM": data["issues_num"],
        "PRS_NUM": data["prs_num"],

        "REPOS_NUM": data["repos_num"],
        "TOP_3_MOST_COMMITTED_REPOS": sorted(
            [
                {"name": repo["name"], "num": repo["commits_num"]}
                for repo in data["repos_details"]
            ],
            key=lambda x: x["num"],
            reverse=True,
        )[: min(3, len(data["repos_details"]))],
        "LANGUAGES_NUM": len(data_new_repo["languages_num"]),
        "TOP_3_LANGUAGES_USED_IN_NEW_REPOS": list(
            [
                {"name": k, "num": v}
                for k, v in data_new_repo["languages_num"].items()
            ],
        )[: min(3, len(data_new_repo["languages_num"]))],
        "CONVENTIONAL_COMMITS_NUM": sum(
            [v for k, v in data["commits_types_num"].items() if k != "others"]
        ),
        "TOP_3_CONVENTIONAL_COMMIT_TYPES": sorted(
            [
                {"name": k, "num": v}
                for k, v in data["commits_types_num"].items()
                if k != "others"
            ],
            key=lambda x: x["num"],
            reverse=True,
        )[: min(3, len(data["commits_types_num"]) - 1)],
    }

    html_output = _render_template("template/template.html", **context)

    if not os.path.exists("dist/assets/img"):
        os.makedirs("dist/assets/img")
    shutil.copy("data/avatar.png", "dist/assets/img/avatar.png")

    with open("dist/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)


def _render_template(template_path, **kwargs):
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    html_content = template.format(**kwargs)
    return html_content
