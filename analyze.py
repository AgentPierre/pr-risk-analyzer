import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_open_prs(owner: str, repo: str) -> list[dict]:
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
    params = {"state": "open", "per_page": 20}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()

    return response.json()


def get_pr_files(owner: str, repo: str, pr_number: int) -> list[dict]:
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()


def parse_pr(pr: dict, files: list[dict]) -> dict:
    return {
        "number": pr["number"],
        "title": pr["title"],
        "author": pr["user"]["login"],
        "description": pr["body"] or "No description provided.",
        "files_changed": len(files),
        "additions": sum(f["additions"] for f in files),
        "deletions": sum(f["deletions"] for f in files),
        "filenames": [f["filename"] for f in files]
    }