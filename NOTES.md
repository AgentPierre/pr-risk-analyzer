# PR Risk Analyzer — Learning Notes

> **How to use this file:**
> Each topic is self-contained. Use the Table of Contents to jump to any concept.
> Every entry includes when it was learned, why it works, and good-to-know context.
> Checkpoints track your answers and growth over time.

---

## Table of Contents

- [The Learning Contract](#the-learning-contract)
- [GIT](#git)
- [LINUX & TERMINAL](#linux--terminal)
- [PYTHON](#python)
- [TESTING](#testing)
- [CI/CD & GITHUB ACTIONS](#cicd--github-actions)
- [TERRAFORM & IAC](#terraform--iac)
- [AZURE](#azure)
- [DEVOPS CONCEPTS](#devops-concepts)
- [AI & PROMPT ENGINEERING](#ai--prompt-engineering)
- [HTTP & APIs](#http--apis)
- [SECRETS MANAGEMENT](#secrets-management)
- [ERRORS & FIXES](#errors--fixes)
- [CHECKPOINTS](#checkpoints)
- [QUESTIONS TO FOLLOW UP ON](#questions-to-follow-up-on)

---

## The Learning Contract

Before running any code, answer these three questions:
1. What does this do?
2. Why is it structured this way?
3. What would break if I removed or changed X?

---

---

# GIT

> 📅 Week 1 | Core skill — used every session

---

### What is Git?
A version control system that tracks every change you make to files over time.
Think of it as a save system for your code — except every save has a message, a timestamp, and can be rewound.

**Why it works:**
Git stores your project history as a chain of snapshots called commits. Each commit points to the previous one, forming a timeline you can always rewind.

**Good to know:**
Git is the industry standard. Your commit history is a professional artifact — future employers and teammates read it.

---

### `git init`
> 📅 Week 1

Initializes a new Git repository in the current folder.

**Why it works:**
Creates a hidden `.git` folder that stores your entire project history. Without it, no other Git commands will work.

**Good to know:**
Only run once per project. Always check you're in the right folder first with `pwd`.

---

### `git status`
> 📅 Week 1

Shows the current state of your working directory.

**Why it works:**
Git tracks three zones:
- **Untracked** — new files Git hasn't seen (shown in red)
- **Staged** — files ready to commit (shown in green)
- **Modified** — tracked files that changed since last commit

**Good to know:**
Run `git status` constantly — before staging, before committing, after pulling. It's your sanity check.

---

### `git add .`
> 📅 Week 1

Stages all changed and new files for the next commit.

**Why it works:**
`.` means "everything from here". Git reads `.gitignore` first and silently skips listed files — so `.env` and `.venv/` are never staged accidentally.

**Good to know:**
Use `git add filename` to stage individual files when you want fine-grained control over what goes into a commit.

---

### `git commit -m "message"`
> 📅 Week 1

Saves a permanent snapshot of everything staged, with a descriptive message.

**Why it works:**
Records who made the change, when, and why. The `-m` flag writes the message inline.

**Good to know:**
Use **Conventional Commits** format — standard on real engineering teams:

| Prefix | Use for |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `chore:` | Maintenance, config changes |
| `refactor:` | Code restructure, no behavior change |

---

### `git push`
> 📅 Week 2

Uploads your local commits to GitHub.

**Why it works:**
Git separates local and remote work deliberately. You commit locally freely, then push when ready to share or back up.

**Good to know:**
`Your branch is ahead of 'origin/master' by N commits` means unpushed local commits exist. Always push before ending a session.

---

### When to Commit
> 📅 Week 1

| Situation | Commit? |
|---|---|
| Code complete, testing for first time | ✅ Yes — save clean state first |
| Mid-debug on a crash | ❌ No — don't commit broken code |
| Just fixed a bug and it works | ✅ Yes — commit the fix |
| Making a tiny tweak to test | ❌ No — wait until it works |
| About to try something risky | ✅ Yes — gives a safe revert point |

**Rule of thumb:** commit working code, not broken code.

---

---

# LINUX & TERMINAL

> 📅 Week 1 | Used every session

---

### The Terminal Mental Model
> 📅 Week 1

The terminal always has a "current location". Every command runs relative to that location.

**Why it works:**
Unlike a GUI, the terminal requires explicit navigation. Your location affects everything — `git init` in the wrong folder, `pip install` outside a venv, or `touch` in the wrong directory all cause silent problems.

**Good to know:**
Run `pwd` whenever something isn't behaving as expected. 90% of the time you're in the wrong folder.

---

### Key Navigation Commands
> 📅 Week 1

| Command | What it does | Why it works |
|---|---|---|
| `cd ~` | Go to home directory | `~` always expands to your home path |
| `cd foldername` | Move into a folder | Changes current working directory |
| `cd ..` | Go up one level | `..` always means parent directory |
| `pwd` | Print current directory | Your GPS in the terminal |
| `mkdir foldername` | Create a new folder | Makes an empty directory |
| `touch filename` | Create an empty file | Originally for timestamps — now used to create files |
| `ls` | List files | Short for "list" |
| `ls -la` | List all files including hidden | `-l` = long format, `-a` = all files |
| `find . -not -path './.git/*'` | List all project files | Recursively lists everything |

---

### Hidden Files (dotfiles)
> 📅 Week 1

Files starting with `.` are hidden by default in Linux (e.g. `.env`, `.gitignore`, `.venv`).

**Why it works:**
Linux convention: a leading dot means "configuration file — don't show by default."

**Good to know:**
Run `ls -la` to see hidden files. In DevOps, most config files are dotfiles — `.bashrc`, `.ssh/`, `.kube/config`.

---

### `source` command
> 📅 Week 1

Runs a script in your **current shell session** rather than a subprocess.

**Why it works:**
Scripts normally run in a child process — changes disappear when it exits. `source` runs the script in your current shell so changes (like activating a venv) stick.

**Good to know:**
Two main uses in DevOps:
1. `source .venv/bin/activate` — activate Python venv
2. `source ~/.bashrc` — reload shell config after editing

---

### nano (Terminal Text Editor)
> 📅 Week 1

| Action | Keys |
|---|---|
| Save | `Ctrl + O` → Enter |
| Exit | `Ctrl + X` |
| Search | `Ctrl + W` |

**Good to know:**
Use nano for quick edits. Use `code filename` for bigger files. `vim` exists on most servers — you'll encounter it, but nano is fine for now.

---

### WSL2
> 📅 Week 1

Runs a real Linux environment inside Windows.

**Why it works:**
WSL2 uses a real Linux kernel inside a lightweight VM. All Linux/DevOps commands work natively.

**Good to know:**
- `wsl` is a Windows-only command — only run it in PowerShell, never Ubuntu
- Access WSL files from Windows at `\\wsl.localhost\Ubuntu\home\username\`
- Access Windows files from WSL at `/mnt/c/Users/username/`

---

---

# PYTHON

> 📅 Week 1–3

---

### Virtual Environments (venv)
> 📅 Week 1

An isolated Python installation for your project.

**Why it works:**
Packages installed inside it don't affect system Python or other projects. Newer Ubuntu versions enforce isolation by blocking direct `pip install`.

**Good to know:**
Every real Python project uses a venv. It's how teams guarantee "it works on my machine" actually means something.

```bash
python3 -m venv .venv          # create (once)
source .venv/bin/activate      # activate (every new terminal)
pip install -r requirements.txt  # install packages
```

---

### `pip` vs `pip3`
> 📅 Week 1

- `pip3` = pip for Python 3 specifically (used when Python 2 and 3 coexist)
- Inside a venv there's only one Python — plain `pip` works

**Good to know:**
Python 2 reached end-of-life in 2020. Inside a venv, never need the `3` suffix.

---

### `import` vs `from x import y`
> 📅 Week 1

- `import requests` — brings in the whole library
- `from dotenv import load_dotenv` — grabs one specific function

**Why it works:**
`from x import y` is more surgical — avoids loading an entire library when you only need one function.

**Good to know:**
Use `from x import y` for specific tools. Use `import x` when you need multiple things from a library.

---

### `load_dotenv()`
> 📅 Week 1

Reads `.env` file and injects its key-value pairs into the environment.

**Why it works:**
`os.getenv()` reads from the process environment, not from files. `load_dotenv()` bridges that gap.

**Good to know:**
Always call it before any `os.getenv()` calls — if called too late, variables won't exist yet.

---

### `raise_for_status()`
> 📅 Week 1

Raises an exception if the HTTP response has an error status code (4xx or 5xx).

**Why it works:**
`requests.get()` succeeds for any response — even failures. Without this, code silently continues with bad data.

**Good to know:**
Common status codes:

| Code | Meaning | Likely cause |
|---|---|---|
| `200` | OK | Everything worked |
| `401` | Unauthorized | Bad or missing token |
| `403` | Forbidden | Token lacks required scope |
| `404` | Not found | Wrong URL or repo name |
| `500` | Server error | Their problem, not yours |

---

### `if __name__ == "__main__":`
> 📅 Week 1

Entry point guard — ensures `main()` only runs when the file is executed directly.

**Why it works:**
Python sets `__name__` to `"__main__"` when run directly. When imported, `__name__` becomes the filename. This one check tells Python the difference.

**Good to know:**
Without this guard, importing `analyze.py` would immediately start fetching PRs. You'll see this at the bottom of almost every Python script.

---

### List Comprehension
> 📅 Week 1

Compact way to build a new list by looping in one line.

```python
# Long version:
filenames = []
for f in files:
    filenames.append(f["filename"])

# List comprehension:
filenames = [f["filename"] for f in files]
```

**Pattern:** `[expression for item in iterable]`

**Good to know:**
Add a filter: `[f["filename"] for f in files if f["status"] != "removed"]`

---

### Generator Expression
> 📅 Week 1

Same as list comprehension but computes a single value instead of building a list.

```python
total = sum(f["additions"] for f in files)
```

**Why it works:**
Yields one value at a time directly to `sum()` — more memory efficient than building an intermediate list.

**Good to know:**
Use inside `sum()`, `max()`, `min()`, `any()`, `all()`.

---

### argparse
> 📅 Week 3

Python library for building CLI tools that accept terminal arguments.

**Why it works:**
Reads `sys.argv` and maps typed arguments to named variables. `--repo microsoft/vscode` becomes `args.repo = "microsoft/vscode"`.

**Good to know:**
- `required=True` — script errors helpfully if argument is missing
- `default=5` — uses fallback value if argument is omitted
- `type=int` — automatically converts string input to integer

```python
parser.add_argument("--limit", type=int, default=5, help="Max PRs to analyze")
# accessed as: args.limit
```

---

### File Output with `with open()`
> 📅 Week 3

Safe way to write results to a file.

**Why it works:**
`with` is a context manager — it guarantees the file closes cleanly even if an error occurs mid-write. Without it, a crash can leave the file handle open and corrupt the output.

**Good to know:**
File modes:
- `"w"` — write (overwrites existing file)
- `"a"` — append (adds to existing file)
- `"r"` — read only

```python
with open(args.output, "w") as f:
    f.write(content)
# file closes automatically here
```

---

---

# TESTING

> 📅 Weekend Sprint (pre-internship)

---

### What is pytest?
> 📅 Weekend Sprint

Python's standard testing framework. Finds and runs any function starting with `test_` automatically.

**Why it works:**
pytest discovers test files matching `test_*.py` or `*_test.py` and runs every function prefixed with `test_`. No boilerplate required — just write functions and assert expected outcomes.

**Good to know:**
Tests prove your code works before CI runs it. Your manager's team runs tests on every commit — showing you already understand this habit matters on day one.

```bash
pytest tests/ -v    # run all tests with verbose output
```

---

### Mock Data in Tests
> 📅 Weekend Sprint

Simulated inputs that mimic real API responses — used so tests run without making actual API calls.

**Why it works:**
Real API calls in tests are slow, cost money, and can fail for reasons unrelated to your code (network issues, rate limits, API changes). Mock data gives you full control — your tests always run fast, free, and consistently.

**Good to know:**
This is called "mocking" — standard practice in every professional codebase. The rule is: unit tests should never touch the network.

```python
MOCK_PR = {
    "number": 1,
    "title": "Test PR",
    "user": {"login": "testuser"},
    "body": "Description here."
}
MOCK_FILES = [
    {"filename": "auth/login.py", "additions": 50, "deletions": 10}
]
```

---

### `assert` statements
> 📅 Weekend Sprint

How pytest verifies your code does what you expect.

**Why it works:**
`assert` evaluates an expression — if it's True, the test passes silently. If it's False, pytest catches the failure and reports exactly what went wrong.

**Good to know:**
Write assertions that test one specific thing per test. A test called `test_parse_pr_counts_additions_correctly` should only assert additions — not titles, authors, and additions all in one.

```python
def test_parse_pr_counts_additions_correctly():
    result = parse_pr(MOCK_PR, MOCK_FILES)
    assert result["additions"] == 55  # 50 + 5 across two files
```

---

### Test File Structure
> 📅 Weekend Sprint

```
tests/
├── __init__.py          # makes tests/ a Python package
└── test_analyzer.py     # test file — must start with test_
```

**Why it works:**
pytest looks for files matching `test_*.py`. The `__init__.py` lets Python treat the folder as a module so imports work correctly.

**Good to know:**
Name test functions descriptively — `test_parse_pr_handles_no_description` tells you exactly what broke without reading the code.

---

---

# CI/CD & GITHUB ACTIONS

> 📅 Weekend Sprint (pre-internship)

---

### What is CI/CD?
> 📅 Week 1 concept, implemented Weekend Sprint

**CI (Continuous Integration):** Automatically run tests every time code is pushed.
**CD (Continuous Delivery):** Automatically deploy when tests pass.

**Why it works:**
Manual deployments are slow, error-prone, and inconsistent. CI/CD pipelines run the same steps every time — catching bugs before they reach production.

**Good to know:**
Your manager's team uses this as the backbone of their cloud operations. CI = "it definitely works", not "I think it works".

---

### GitHub Actions
> 📅 Weekend Sprint

GitHub's built-in CI/CD system. Defined in YAML files under `.github/workflows/`.

**Why it works:**
Every push to GitHub triggers the workflow automatically. GitHub spins up a fresh cloud VM, runs your steps, and reports pass/fail directly in your repo.

**Good to know:**
Free for public repos. The workflow file is version-controlled alongside your code — so your CI config has the same history as everything else.

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [ main, master ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pytest
      - run: pytest tests/ -v
```

---

### Why `ubuntu-latest` in CI?
> 📅 Weekend Sprint

CI pipelines use `ubuntu-latest` instead of your local machine setup.

**Why it works:**
Production servers almost always run Linux. Using `ubuntu-latest` means tests run in an environment close to production — not your personal machine with its unique config. This is the "it works everywhere" guarantee CI provides.

**Good to know:**
GitHub Actions supports Windows and macOS runners too — but Linux is the default for backend/DevOps work because it matches what runs in the cloud.

---

### CI vs Azure Pipelines
> 📅 Weekend Sprint

| | GitHub Actions | Azure Pipelines |
|---|---|---|
| Where config lives | `.github/workflows/` | `azure-pipelines.yml` |
| Trigger | Push to GitHub | Push to Azure DevOps Repos |
| Free tier | Yes (public repos) | Yes (up to 5 users) |
| Your team uses | GitHub Actions (this project) | Azure Pipelines (internship) |

**Good to know:**
The concepts are identical — YAML config, triggered on push, runs steps in order. The syntax differs slightly. Your GitHub Actions experience maps directly to Azure Pipelines on day one.

---

---

# TERRAFORM & IAC

> 📅 Weekend Sprint (pre-internship)

---

### What is Terraform?
> 📅 Weekend Sprint

An open-source Infrastructure as Code tool that lets you define cloud resources in configuration files and provision them automatically.

**Why it works:**
Instead of clicking through the Azure portal to create resources, you write a `.tf` file describing what you want. Terraform figures out what needs to be created, modified, or destroyed to match your description.

**Good to know:**
Your manager specifically named Terraform as the team standard. The goal: environments should be buildable, tear-downable, and rebuildable via Terraform + automated pipelines.

---

### Core Terraform Commands
> 📅 Weekend Sprint

| Command | What it does |
|---|---|
| `terraform init` | Downloads provider plugins (run once per project) |
| `terraform plan` | Shows what would change — safe, no modifications made |
| `terraform apply` | Actually creates/modifies/destroys resources |
| `terraform destroy` | Tears down all resources defined in config |
| `terraform validate` | Checks syntax without connecting to cloud |

**Good to know:**
Always run `terraform plan` before `terraform apply`. It's your preview — like a git diff before committing.

---

### Terraform File Structure
> 📅 Weekend Sprint

```
main.tf              # resource definitions
variables.tf         # input variable declarations
terraform.tfvars     # actual variable values (don't commit secrets)
terraform.tfvars.example  # safe template to commit
```

**Why it works:**
Separating definitions from values means the same config works across dev, staging, and prod by swapping `.tfvars` files.

**Good to know:**
`terraform.tfvars` is like `.env` for Terraform — add it to `.gitignore` if it contains real values.

---

### AWS → Azure Resource Mapping (for Terraform)
> 📅 Weekend Sprint

| AWS (what you know) | Azure Terraform resource |
|---|---|
| AWS Account/Region scope | `azurerm_resource_group` |
| AWS Secrets Manager | `azurerm_key_vault` |
| ECS / Fargate | `azurerm_container_group` |
| ECR | `azurerm_container_registry` |
| IAM Role | `azurerm_role_assignment` |
| VPC | `azurerm_virtual_network` |

**Good to know:**
The Terraform syntax is identical regardless of cloud provider — only the resource names and properties change. Your Terraform knowledge from this project transfers directly to AWS, GCP, or any other provider.

---

---

# AZURE

> 📅 Weekend Sprint (pre-internship) | Deep dive on the job

---

### Azure for Students
> 📅 Weekend Sprint

Free Azure access for university students — $100 credits, no credit card required.

**How to get it:** azure.microsoft.com/en-us/free/students — sign up with your `.edu` email.

---

### AWS → Azure Concept Map
> 📅 Weekend Sprint

Your AWS CCP knowledge transfers directly — just learn Microsoft's names:

| AWS | Azure |
|---|---|
| AWS Account | Subscription |
| IAM Roles/Policies | Azure RBAC |
| CloudFormation | ARM Templates / Terraform |
| EC2 | Virtual Machines |
| ECS/Fargate | Container Instances |
| ECR | Container Registry |
| Secrets Manager | Key Vault |
| CodePipeline | Azure Pipelines |
| S3 | Blob Storage |
| VPC | Virtual Network |

---

### Azure DevOps
> 📅 Weekend Sprint

Microsoft's platform for version control, CI/CD pipelines, and project management — all in one place.

**Why it works:**
Azure DevOps bundles Git repos (Azure Repos), CI/CD (Azure Pipelines), work tracking (Azure Boards), and artifact storage (Azure Artifacts). Your internship team uses this as their primary platform.

**Good to know:**
Thomas's day-to-day: helping teams commit code to Azure Repos, setting up pipelines that deploy to Azure subscriptions, and managing access control. Understanding this context on day one matters.

---

### Azure Resource Groups
> 📅 Weekend Sprint

Logical containers that hold related Azure resources — like a folder for your cloud infrastructure.

**Why it works:**
Every Azure resource must belong to a resource group. It lets you manage, monitor, and delete related resources together. Like an AWS account scope but more granular.

**Good to know:**
Thomas mentioned subscriptions constantly in the coffee chat. A subscription contains resource groups, which contain resources. Know this hierarchy: **Tenant → Subscription → Resource Group → Resource**.

---

### Azure Key Vault
> 📅 Weekend Sprint

Azure's secrets management service — stores API keys, tokens, and passwords securely.

**Why it works:**
Apps read secrets from Key Vault at runtime instead of storing them in code or config files. Access is controlled by Azure RBAC — only authorized identities can read specific secrets.

**Good to know:**
This is where your team would store the GitHub PAT and Claude API key in a real deployment — not in a `.env` file.

---

---

# DEVOPS CONCEPTS

> 📅 Week 1–3 | Core internship focus

---

### Infrastructure as Code (IaC)
> 📅 Introduced Week 1, implemented Weekend Sprint

The practice of managing and provisioning infrastructure through code rather than manual processes.

**Why it works:**
Code is repeatable, versionable, and auditable. A Terraform file that defines a server can be run 100 times and produce the same result — a human clicking through a portal cannot guarantee that.

**Good to know:**
Key benefits your manager named:
- **Repeatability** — reduces drift and "it works on my machine" issues
- **Speed + safety** — faster recovery, lower blast radius when changes fail
- **Auditability** — clear history of what changed and why
- **Scale** — less manual toil, more time on reliability

---

### PR Risk Analysis
> 📅 Week 1–2

The practice of evaluating how risky a pull request is before merging it.

**Why it works:**
Not all changes carry equal risk. A 10-line change to auth logic is riskier than a 500-line README update. Automated risk analysis scales this judgment across hundreds of PRs.

**Good to know:**
Risk signals to watch for:

| Signal | Risk implication |
|---|---|
| Auth/security files touched | High — regardless of line count |
| Many files changed | Wide blast radius |
| High additions, low deletions | Lots of new code, little cleanup |
| No description | Less reviewer context |
| Tests included | Lower risk — author verified changes |
| Draft PR | Not ready to merge |

---

---

# AI & PROMPT ENGINEERING

> 📅 Week 2

---

### What is Prompt Engineering?
> 📅 Week 2

The practice of structuring text inputs to AI models to get reliable, useful outputs.

**Why it works:**
AI models respond to context. A well-structured prompt with a clear role, format constraint, and data produces consistently better results than a vague question.

**Good to know:**
This is a real skill your manager's team uses. Getting good at it is genuinely valuable on the job — especially when building internal tools.

---

### The Three-Part Prompt Structure
> 📅 Week 2

Every good AI prompt for a tool has three parts:

1. **Role** — "You are a senior DevOps engineer" sets the reasoning perspective
2. **Format constraint** — asking for JSON means you can parse the response programmatically
3. **Data** — the actual content Claude needs to make a judgment

**Good to know:**
Always ask for the minimum output fields you need. Extra fields cost tokens, which costs money at scale.

---

### Why JSON Output Format Matters
> 📅 Week 2

Asking for JSON instead of plain text means you can parse the response with `json.loads()`.

**Why it works:**
Plain text like "I think this is high risk" has no reliable structure to extract from. `{"risk_level": "HIGH"}` is always parseable the same way.

---

### Cleaning AI Responses Before Parsing
> 📅 Week 2

Claude sometimes wraps JSON in markdown code fences. Always strip before calling `json.loads()`.

**Why it works:**
Triple backticks are markdown syntax — not valid JSON. `json.loads()` fails with `JSONDecodeError` if they're present.

```python
raw = raw.strip()
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()
```

---

### API Costs
> 📅 Week 2

Each Claude API call costs fractions of a cent. At scale, small costs compound.

**Why it works:**
Pay-per-use APIs charge by tokens (~1 token ≈ 4 characters). Your prompt + response = total tokens billed.

**Good to know:**
Cost optimization strategies used on real teams:
- Choose a smaller model for simpler tasks
- Minimize prompt length — only send what's needed
- Cache results for unchanged PRs
- Batch calls where possible

---

---

# HTTP & APIs

> 📅 Week 1–2

---

### HTTP Headers
> 📅 Week 1

Key-value pairs sent with every API request describing who is asking and what they want back.

**Why it works:**
The server reads headers to decide whether to accept the request and how to format the response.

**Good to know:**
CORS is a browser security concept — it does NOT apply to Python scripts.

| Header | Purpose |
|---|---|
| `Authorization: Bearer <token>` | Prove identity |
| `Accept: application/json` | Request JSON format |
| `Content-Type: application/json` | Declare you're sending JSON |
| `X-Request-ID` | Trace requests across distributed systems |

---

### GitHub Personal Access Token (PAT)
> 📅 Week 1

A scoped token that grants API access to GitHub on your behalf.

**Why it works:**
GitHub disabled password auth for API calls in 2021. Tokens are safer — scoped to specific permissions and revocable without changing your password.

**Good to know:**
- Set minimum scope needed — `repo` read for this project
- Tokens expire — regenerate before internship starts
- Never hardcode in source files
- If accidentally committed — revoke immediately and generate a new one

---

---

# SECRETS MANAGEMENT

> 📅 Week 1

---

### `.env` File
> 📅 Week 1

Stores sensitive values (tokens, API keys) outside of source code.

**Why it works:**
Code reads values from the environment at runtime — not from the file directly. Different environments (dev, staging, prod) can have different values without touching code.

**Good to know:**
On real teams, production secrets live in AWS Secrets Manager, Azure Key Vault, or GitHub Actions secrets — never `.env` files.

---

### `.gitignore`
> 📅 Week 1

Tells Git which files to never track, stage, or commit — ever.

**Why it works:**
Git checks `.gitignore` before staging. Matching files are silently skipped even with `git add .`. Covers the entire `.env` file — adding new secrets never requires updating `.gitignore`.

**Good to know:**
Write `.gitignore` before your first commit. A committed secret lives in Git history permanently — removing it requires rewriting history.

---

---

# ERRORS & FIXES

> 📅 Week 1–3 | Running log of every error encountered

---

### `error: externally-managed-environment`
> 📅 Week 1

- **Cause:** Ubuntu protects system Python from direct `pip install`
- **Fix:** Use a virtual environment
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

---

### `wsl: command not found`
> 📅 Week 1

- **Cause:** Ran a Windows-only command inside Ubuntu terminal
- **Fix:** Open PowerShell and run it there

---

### `bash: /path/to/folder: Is a directory`
> 📅 Week 1

- **Cause:** Typed a folder path as a command — forgot `cd`
- **Fix:** `cd /home/perry/Projects/pr-risk-analyzer`

---

### `bash: .venv/bin/activate: No such file or directory`
> 📅 Week 1

- **Cause:** Tried to activate venv from wrong directory
- **Fix:** `cd` into the project folder first

---

### Git identity error on first commit
> 📅 Week 1

- **Cause:** Git doesn't know who you are yet
- **Fix:**
```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

---

### `Command 'python' not found`
> 📅 Week 1

- **Cause:** Ubuntu only ships with `python3`
- **Fix:** Always use `python3` to run scripts

---

### VS Code `Import "dotenv" could not be resolved`
> 📅 Week 1

- **Cause:** VS Code pointing at system Python instead of venv
- **Fix:** `Ctrl + Shift + P` → `Python: Select Interpreter` → select `.venv`

---

### `json.decoder.JSONDecodeError: Expecting value`
> 📅 Week 2

- **Cause:** Claude wrapped JSON response in markdown code fences
- **Fix:** Strip code fences before `json.loads()`

---

### `anthropic.BadRequestError: credit balance too low`
> 📅 Week 2

- **Cause:** No credits on Anthropic account
- **Fix:** console.anthropic.com → Plans & Billing → add credits

---

### `usage: analyze.py [-h] --repo REPO`
> 📅 Week 3

- **Cause:** Running old version of analyze.py that didn't have --limit flag yet
- **Fix:** Make sure analyze.py has the updated argparse section with `--limit` and `--output` arguments

---

---

# CHECKPOINTS

---

## Week 1 — Environment & GitHub Client
> 📅 Week 1 ✅ Complete

| Question | Your Answer | Verdict |
|---|---|---|
| What does `load_dotenv()` do? | Reads the .env file and loads values so `os.getenv()` can access them | ✅ Correct |
| What does `raise_for_status()` do? | Raises an error immediately if the request returned 4xx or 5xx | ✅ Correct |
| What is a generator expression? | A compact way to loop and compute a value in one line | ✅ Correct |
| What is a virtual environment? | Isolates project packages from the system Python | ✅ Correct |
| What does `source .venv/bin/activate` do? | Activates the venv from the source of the folder | 🟡 Half right — `source` runs it in your current shell so changes stick |
| Why `pip` not `pip3` inside a venv? | pip is the default syntax for a venv | 🟡 Close — only one Python inside a venv so the `3` is unnecessary |
| What do the three `import` lines do? | `requests` = HTTP library, `os` = OS tools, `from dotenv import load_dotenv` = grab one function | ✅ Mostly correct |
| What is `HEADERS` and why send it? | CORS to accept the GitHub token request | 🟡 Wrong concept — CORS is browser-only. `HEADERS` proves identity + sets response format |
| What is `[f["filename"] for f in files]`? | Finds the filenames in the list called files | ✅ Correct — called a list comprehension |
| What does `if __name__ == "__main__":` do? | It's the entry point for the code | ✅ Correct — only runs when executed directly, not when imported |
| What determines PR risk? | The one with the most additions and deletions | ✅ Good instinct — line count is a signal, but file type and context matter too |

---

## Week 2 — AI Integration
> 📅 Week 2 ✅ Complete

| Question | Your Answer | Verdict |
|---|---|---|
| Why send filenames to Claude, not just line counts? | Because filenames tell Claude what kind of code changed — auth files are riskier than docs | ✅ Correct |
| Why ask Claude for JSON instead of plain text? | So we can reliably parse the response with `json.loads()` and extract specific fields | ✅ Correct |
| Why does per-call API cost matter? | At scale, small per-call costs add up — real teams monitor and optimize AI API spend | ✅ Correct |

---

## Week 3 — CLI Polish
> 📅 Week 3 ✅ Complete

| Question | Your Answer | Verdict |
|---|---|---|
| What happens if you run without --limit? | Uses default value of 5, analyzes first 5 PRs | ✅ Correct |
| Why use `with open()` instead of plain `open()`? | `with` automatically closes the file when the block ends, even if an error occurs | ✅ Correct |

---

## Weekend Sprint — Tests, CI, Terraform, Azure
> 📅 Weekend Sprint 🔄 In progress

| Question | Your Answer | Verdict |
|---|---|---|
| What is mock data and why use it in tests? | Simulates GitHub API responses so tests run without real API calls | ✅ Correct |
| Why does CI use `ubuntu-latest` instead of your local setup? | To guarantee a clean consistent environment that matches production servers | ✅ Correct |
| What Azure service maps to AWS CodePipeline? | Azure Pipelines | ✅ Correct |

---

---

# QUESTIONS TO FOLLOW UP ON

> Review these before or during your internship

- [ ] What is the difference between a `GET` and a `POST` request?
- [ ] Why does GitHub's API use `Bearer` tokens instead of passing the token directly?
- [ ] What happens to your Git history if you commit a secret by accident?
- [ ] What is `git diff` and when would you use it?
- [ ] What is token length and how does it affect AI API cost?
- [ ] How would you cache AI responses to avoid paying for the same PR twice?
- [ ] What is `terraform apply` doing under the hood?
- [ ] What is the difference between Azure Pipelines and GitHub Actions YAML syntax?
- [ ] What is Docker and why do teams containerize applications?
- [ ] What is Azure RBAC and how does least privilege work in Azure?

---

*Last updated: Week 3 ✅ | Weekend Sprint in progress*
