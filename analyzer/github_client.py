import requests
import os
from dotenv import load_dotenv

# load environment variables from .env so we can access the GitHub token
load_dotenv()

# grab the token from the environment — never hardcoded
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

# sent with every request to prove identity and tell GitHub what format to send back
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_open_prs(owner: str, repo: str) -> list[dict]:
    # build the GitHub API URL using the owner and repo name
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"

    # params act as filters — only return open PRs, max 20 at a time
    params = {"state": "open", "per_page": 20}

    response = requests.get(url, headers=HEADERS, params=params)

    # raise an error immediately if the request failed (4xx or 5xx)
    response.raise_for_status()

    # return the response as a Python list of PR objects
    return response.json()


def get_pr_files(owner: str, repo: str, pr_number: int) -> list[dict]:
    # use the PR number (e.g. #42) to get the files changed in that specific PR
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()


def parse_pr(pr: dict, files: list[dict]) -> dict:
    # GitHub sends PR metadata and file data as separate responses
    # this function pulls out only the fields we care about and combines them
    return {
        "number": pr["number"],
        "title": pr["title"],
        "author": pr["user"]["login"],
        "description": pr["body"] or "No description provided.",
        # count how many files were touched
        "files_changed": len(files),
        # sum up all line additions and deletions across every file
        "additions": sum(f["additions"] for f in files),
        "deletions": sum(f["deletions"] for f in files),
        # build a list of just the filenames
        "filenames": [f["filename"] for f in files]
    }