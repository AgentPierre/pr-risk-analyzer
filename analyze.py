import argparse
import json
from datetime import datetime
from analyzer.github_client import get_open_prs, get_pr_files, parse_pr
from analyzer.ai_analyzer import analyze_pr_risk
# risk level emoji labels for display
RISK_EMOJI = {
    "LOW": "🟢 LOW",
    "MEDIUM": "🟡 MEDIUM",
    "HIGH": "🔴 HIGH"
}
def format_pr(parsed, analysis):
    # build a formatted string for one PR result
    risk = RISK_EMOJI.get(analysis.get("risk_level", "MEDIUM"))
    summary = analysis.get("summary", "No summary available.")
    lines = [
        f"PR #{'{'}parsed['number']{'}'} — {'{'}parsed['title']{'}'}",
        f"  Author       : {'{'}parsed['author']{'}'}",
        f"  Files changed: {'{'}parsed['files_changed']{'}'}",
        f"  Additions    : +{'{'}parsed['additions']{'}'}",
        f"  Deletions    : -{'{'}parsed['deletions']{'}'}",
        f"  Risk Level   : {'{'}risk{'}'}",
        f"  Summary      : {'{'}summary{'}'}",
        ""
    ]
    return "\n".join(lines)
def main():
    # set up CLI arguments
    parser = argparse.ArgumentParser(description="Analyze open PRs in a GitHub repo.")
    parser.add_argument("--repo", required=True, help="Format: owner/repo-name")
    parser.add_argument("--limit", type=int, default=5, help="Max PRs to analyze (default: 5)")
    parser.add_argument("--output", help="Save results to this file e.g. report.txt")
    args = parser.parse_args()
    # split owner/repo into two variables
    owner, repo = args.repo.split("/")
    print(f"\nFetching open PRs from {'{'}owner{'}'}/{'{'}repo{'}'}...\n")
    # fetch PRs and slice to the limit
    prs = get_open_prs(owner, repo)
    prs = prs[:args.limit]
    if not prs:
        print("No open PRs found.")
        return
    results = []
    for pr in prs:
        files = get_pr_files(owner, repo, pr["number"])
        parsed = parse_pr(pr, files)
        print(f"Analyzing PR #{'{'}parsed['number']{'}'}...")
        analysis = analyze_pr_risk(parsed)
        result = format_pr(parsed, analysis)
        print(result)
        results.append(result)
    # save to file if --output was passed
    if args.output:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        header = f"PR Risk Report — {'{'}owner{'}'}/{'{'}repo{'}'}\nGenerated: {'{'}timestamp{'}'}\n{'='*60}\n\n"
        with open(args.output, "w") as f:
            f.write(header)
            f.write("\n".join(results))
        print(f"\n✅ Report saved to {'{'}args.output{'}'}")
if __name__ == "__main__":
    main()