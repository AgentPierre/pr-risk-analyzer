# PR Risk Analyzer

A Python CLI tool that fetches open pull requests from a GitHub repository
and uses Claude AI to rate each PR's risk level and summarize what changed.

Built to mirror real DevOps team workflows — specifically the practice of
using AI to flag and rate risk on upcoming change requests.

---

## What it does

- Connects to GitHub's API to fetch open PRs
- Sends each PR's data (title, files changed, additions, deletions) to Claude AI
- Returns a risk rating: 🟢 LOW / 🟡 MEDIUM / 🔴 HIGH
- Prints a plain-English summary of what changed and why it's risky
- Optionally exports results to a report file

---

## Setup

```bash
# Clone the repo
git clone https://github.com/AgentPierre/pr-risk-analyzer
cd pr-risk-analyzer

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API keys to .env
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN and ANTHROPIC_API_KEY
```

---

## Usage

```bash
# Analyze 5 PRs (default)
python3 analyze.py --repo owner/repo-name

# Analyze a specific number of PRs
python3 analyze.py --repo owner/repo-name --limit 10

# Save results to a file
python3 analyze.py --repo owner/repo-name --limit 5 --output report.txt
```

---

## Example Output

```
PR #316189 — BYOK: Custom Endpoint provider
  Author       : vijayupadya
  Files changed: 9
  Additions    : +694
  Deletions    : -54
  Risk Level   : 🔴 HIGH
  Summary      : Modifies core authentication logic across 9 files.
                 Significant scope with potential for breaking changes.
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Infrastructure (Terraform)

A Terraform configuration for deploying to Azure is included in `main.tf`.
It provisions an Azure Resource Group, Key Vault for secrets, and a
Container Instance to run the analyzer.

```bash
terraform init
terraform plan
# terraform apply  # only when ready to deploy
```

---

## Tech Stack

- Python 3.11
- GitHub REST API
- Anthropic Claude API
- Terraform (Azure)
- GitHub Actions CI