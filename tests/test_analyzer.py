# tests/test_analyzer.py

from analyzer.github_client import parse_pr

# mock data that mimics what GitHub's API returns
MOCK_PR = {
    "number": 1,
    "title": "Test PR",
    "user": {"login": "testuser"},
    "body": "This is a test PR description."
}

MOCK_FILES = [
    {"filename": "auth/login.py", "additions": 50, "deletions": 10},
    {"filename": "README.md", "additions": 5, "deletions": 2}
]


def test_parse_pr_returns_correct_fields():
    # verify parse_pr extracts the fields we expect
    result = parse_pr(MOCK_PR, MOCK_FILES)
    assert result["number"] == 1
    assert result["title"] == "Test PR"
    assert result["author"] == "testuser"
    assert result["files_changed"] == 2


def test_parse_pr_counts_additions_correctly():
    # verify additions are summed across all files
    result = parse_pr(MOCK_PR, MOCK_FILES)
    assert result["additions"] == 55


def test_parse_pr_counts_deletions_correctly():
    # verify deletions are summed across all files
    result = parse_pr(MOCK_PR, MOCK_FILES)
    assert result["deletions"] == 12


def test_parse_pr_handles_no_description():
    # verify fallback when PR has no description
    pr_no_desc = {**MOCK_PR, "body": None}
    result = parse_pr(pr_no_desc, MOCK_FILES)
    assert result["description"] == "No description provided."


def test_parse_pr_extracts_filenames():
    # verify filenames are collected into a list
    result = parse_pr(MOCK_PR, MOCK_FILES)
    assert "auth/login.py" in result["filenames"]
    assert "README.md" in result["filenames"]