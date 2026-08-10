import requests
import os
from dotenv import load_dotenv

BASE_URL = "https://api.github.com"


def _load_github_token() -> str | None:
    # Prefer the current .env value over any stale shell export.
    load_dotenv(override=True)
    return os.getenv("GITHUB_TOKEN")


def _build_headers(use_auth: bool = True) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if use_auth:
        token = _load_github_token()
        if token:
            auth_scheme = "Bearer" if token.startswith("github_pat_") else "token"
            headers["Authorization"] = f"{auth_scheme} {token}"
    return headers


def _github_get(url: str, *, params: dict | None = None, auth_retry: bool = True) -> requests.Response:
    response = requests.get(url, headers=_build_headers(), params=params)
    if response.status_code == 401 and auth_retry and "Authorization" in response.request.headers:
        response = requests.get(url, headers=_build_headers(use_auth=False), params=params)
    return response


def _search_open_prs(owner: str, repo: str) -> list[dict]:
    url = f"{BASE_URL}/search/issues"
    params = {
        "q": f"repo:{owner}/{repo} is:pr is:open",
        "per_page": 20,
    }
    response = _github_get(url, params=params)
    if response.status_code == 401:
        raise requests.HTTPError(
            "GitHub rejected the request with 401 Unauthorized. Check that GITHUB_TOKEN is valid, or remove it for public repositories.",
            response=response,
        )
    response.raise_for_status()
    return response.json().get("items", [])


def get_open_prs(owner: str, repo: str) -> list[dict]:
    # build the GitHub API URL using the owner and repo name
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"

    # params act as filters — only return open PRs, max 20 at a time
    params = {"state": "open", "per_page": 20}

    response = _github_get(url, params=params)

    # raise an error immediately if the request failed (4xx or 5xx)
    if response.status_code == 401:
        raise requests.HTTPError(
            "GitHub rejected the request with 401 Unauthorized. Check that GITHUB_TOKEN is valid, or remove it for public repositories.",
            response=response,
        )
    if response.status_code == 404:
        return _search_open_prs(owner, repo)
    response.raise_for_status()

    # return the response as a Python list of PR objects
    return response.json()


def get_pr_files(owner: str, repo: str, pr_number: int) -> list[dict]:
    # use the PR number (e.g. #42) to get the files changed in that specific PR
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = _github_get(url)
    if response.status_code == 401:
        raise requests.HTTPError(
            "GitHub rejected the request with 401 Unauthorized. Check that GITHUB_TOKEN is valid, or remove it for public repositories.",
            response=response,
        )
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