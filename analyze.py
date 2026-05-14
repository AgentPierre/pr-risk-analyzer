import argparse
import json
from analyzer.github_client import get_open_prs, get_pr_files, parse_pr
from analyzer.ai_analyzer import analyze_pr_risk

# risk level emoji labels for display
RISK_EMOJI = {
    "LOW": "🟢 LOW",
    "MEDIUM": "🟡 MEDIUM",
    "HIGH": "🔴 HIGH"
}


def main():
    # set up the CLI so we can pass --repo from the terminal
    parser = argparse.ArgumentParser(description="Analyze open PRs in a GitHub repo.")
    parser.add_argument("--repo", required=True, help="Format: owner/repo-name")
    args = parser.parse_args()

    # split "owner/repo" into two separate variables
    owner, repo = args.repo.split("/")

    print(f"\nFetching open PRs from {owner}/{repo}...\n")

    # fetch all open PRs from the GitHub API
    prs = get_open_prs(owner, repo)

    if not prs:
        print("No open PRs found.")
        return

    # loop through each PR, fetch its files, parse it, analyze risk, and print
    for pr in prs:
        files = get_pr_files(owner, repo, pr["number"])
        parsed = parse_pr(pr, files)

        # send PR data to Claude and get back risk level + summary
        print(f"Analyzing PR #{parsed['number']}...")
        analysis = analyze_pr_risk(parsed)

        risk = RISK_EMOJI.get(analysis.get("risk_level", "MEDIUM"))
        summary = analysis.get("summary", "No summary available.")

        print(f"\nPR #{parsed['number']} — {parsed['title']}")
        print(f"  Author       : {parsed['author']}")
        print(f"  Files changed: {parsed['files_changed']}")
        print(f"  Additions    : +{parsed['additions']}")
        print(f"  Deletions    : -{parsed['deletions']}")
        print(f"  Risk Level   : {risk}")
        print(f"  Summary      : {summary}")
        print()


if __name__ == "__main__":
    main()