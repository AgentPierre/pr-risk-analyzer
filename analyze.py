import argparse
from analyzer.github_client import get_open_prs, get_pr_files, parse_pr


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

    # loop through each PR, fetch its files, parse it, and print a summary
    for pr in prs:
        files = get_pr_files(owner, repo, pr["number"])
        parsed = parse_pr(pr, files)

        print(f"PR #{parsed['number']} — {parsed['title']}")
        print(f"  Author       : {parsed['author']}")
        print(f"  Files changed: {parsed['files_changed']}")
        print(f"  Additions    : +{parsed['additions']}")
        print(f"  Deletions    : -{parsed['deletions']}")
        print(f"  Files        : {', '.join(parsed['filenames'][:5])}")
        print()


# only run main() when this file is executed directly
# if another file imports this, main() won't fire automatically
if __name__ == "__main__":
    main()