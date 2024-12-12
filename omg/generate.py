import json
import shutil

def generate_site(year: int):
    data = None
    with open("data/result.json", "r") as f:
        data = json.load(f)
    data_new_repo = None
    with open("data/result_new_repo.json", "r") as f:
        data_new_repo = json.load(f)

    USERNAME = data["account_info"]["username"]
    NAME = data["account_info"]["name"]
    AVATAR = data["account_info"]["avatar"]
    BIO = data["account_info"]["bio"]
    CREATED_TIME = data["account_info"]["created_time"]

    FOLLOWERS_NUM = data["account_info"]["followers_num"]
    FOLLOWING_NUM = data["account_info"]["following_num"]

    COMMITS_NUM = data["commits_num"]
    COMMITS_TYPES_NUM = data["commits_types_num"]
    COMMITS_PER_MONTH = data["commits_monthly_num"]
    COMMITS_NUM_OF_MOST_COMMITTED_MONTH = max(COMMITS_PER_MONTH)
    MOST_COMMITTED_MONTH = COMMITS_PER_MONTH.index(COMMITS_NUM_OF_MOST_COMMITTED_MONTH) + 1
    COMMITS_NUM_OF_LEAST_COMMITTED_MONTH = min(COMMITS_PER_MONTH)
    LEAST_COMMITTED_MONTH = COMMITS_PER_MONTH.index(COMMITS_NUM_OF_LEAST_COMMITTED_MONTH) + 1
    COMMITS_PER_WEEKDAY = data["commits_weekdaily_num"]
    MOST_COMMITTED_WEEKDAY = COMMITS_PER_WEEKDAY.index(max(COMMITS_PER_WEEKDAY))
    COMMITS_NUM_OF_MOST_COMMITTED_WEEKDAY = max(COMMITS_PER_WEEKDAY)
    LEAST_COMMITTED_WEEKDAY = COMMITS_PER_WEEKDAY.index(min(COMMITS_PER_WEEKDAY))
    COMMITS_NUM_OF_LEAST_COMMITTED_WEEKDAY = min(COMMITS_PER_WEEKDAY)
    COMMITS_PER_DAY = data["commits_daily_num"][str(year)]
    COMMITS_PER_HOUR = data["commits_hourly_num"]
    MOST_COMMITTED_HOUR = COMMITS_PER_HOUR.index(max(COMMITS_PER_HOUR))
    COMMITS_NUM_OF_MOST_COMMITTED_HOUR = max(COMMITS_PER_HOUR)
    LEAST_COMMITTED_HOUR = COMMITS_PER_HOUR.index(min(COMMITS_PER_HOUR))
    COMMITS_NUM_OF_LEAST_COMMITTED_HOUR = min(COMMITS_PER_HOUR)
    MOST_COMMITTED_REPO = sorted(data["repos_details"], key=lambda x: x["commits_num"], reverse=True)[0]["name"]
    COMMITS_NUM_OF_MOST_COMMITTED_REPO = sorted(data["repos_details"], key=lambda x: x["commits_num"], reverse=True)[0]["commits_num"]

    REPOS_NUM = data["repos_num"]
    NEW_REPOS_NUM = data_new_repo["repos_num"]

    NUMBER_OF_LANGUAGES_USED_IN_NEW_REPOS = len(data_new_repo["repos_languages_num"])
    MOST_USED_LANGUAGE_IN_NEW_REPOS = list(data_new_repo["repos_languages_num"].keys())[0]
    TOP_3_LANGUAGES_USED_IN_NEW_REPOS = list(data_new_repo["repos_languages_num"].keys())[:min(3, len(data_new_repo["repos_languages_num"]))]

    context = {
        "YEAR": year,
        "USERNAME": USERNAME,
        "NAME": NAME,
        "BIO": BIO,
        "COMMITS_PER_DAY": COMMITS_PER_DAY,
        "COMMITS_PER_MONTH": COMMITS_PER_MONTH,
        "COMMITS_PER_WEEKDAY": COMMITS_PER_WEEKDAY,
        "COMMITS_PER_HOUR": COMMITS_PER_HOUR,
        "COMMITS_NUM": COMMITS_NUM,
        "ISSUES_NUM": data["issues_num"],
        "PRS_NUM": data["prs_num"],
        "PRS_MERGED_NUM": data["prs_merged_num"],
        "STARS_NUM": data["stars_num"],
    }

    html_output = _render_template("assets/template.html", **context)
    
    shutil.copy("assets/avatar.png", "dist/assets/img/avatar.png")

    with open("dist/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)


def _render_template(template_path, **kwargs):
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    html_content = template.format(**kwargs)
    return html_content
