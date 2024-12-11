import requests
from datetime import datetime
import os
import re
import json
from typing import Dict, List, Tuple, Any
from dotenv import load_dotenv
import urllib.parse

def get_commit_type(message: str) -> str:
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