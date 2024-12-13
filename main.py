import os
from dotenv import load_dotenv
import json

from util import Github
from omg.generate import generate_site
from omg.fetch import fetch_github

def load_constants(username: str, year: int):
    global ACCESS_TOKEN
    load_dotenv()
    ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

    global USERNAME
    USERNAME = username

    global YEAR
    YEAR = year

    global TIMEZONE
    TIMEZONE = "Asia/Shanghai"

if __name__ == "__main__":
    load_constants("WCY-dt", 2024)

    github = Github(access_token=ACCESS_TOKEN, username=USERNAME, timezone=TIMEZONE)

    fetch_github(github, YEAR, skip_fetch=False)

    generate_site(YEAR)
