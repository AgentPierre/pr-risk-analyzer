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
- [DOCKER](#docker)
- [SECURITY & SECRETS](#security--secrets)
- [DEVOPS CONCEPTS](#devops-concepts)
- [AI & PROMPT ENGINEERING](#ai--prompt-engineering)
- [HTTP & APIs](#http--apis)
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

## Project Status — ✅ COMPLETE & CLOSED OUT

| Phase | Status | Key Outcome |
|---|---|---|
| Week 1 — GitHub API client | ✅ | Fetches real PRs via REST API |
| Week 2 — Claude AI integration | ✅ | Rates PR risk LOW/MEDIUM/HIGH |
| Week 3 — CLI polish | ✅ | --limit and --output flags |
| Weekend Sprint — Tests & CI | ✅ | pytest suite + GitHub Actions |
| Infrastructure — Terraform | ✅ | Resource Group, Key Vault, ACR, Container Instances, Log Analytics deployed |
| Docker | ✅ | Image builds locally and pushed to ACR |
| Refactor — production-ready imports | ✅ | load_dotenv() moved to entrypoint |
| Azure deployment | ✅ | Live resources in East US |
| Secrets — Key Vault | ✅ | ANTHROPIC_API_KEY and GITHUB_TOKEN stored in Key Vault |
| Service Principal | ✅ | Non-personal Azure auth for CI/CD, .edu account never touched |
| CI/CD Pipeline — Full | ✅ | Tests → Terraform Apply → Build → Push ACR → Deploy ACI on every push |
| Remote Terraform state | ✅ | Azure Blob Storage backend — shared between local and CI |
| Log Analytics | ✅ | Deployed for future log persistence beyond container termination |

**Final pipeline run: all 3 jobs green (Run Tests → Terraform Apply → Build, Push, Deploy)**

## Quantifiable Metrics

| Metric | Value |
|---|---|
| Test coverage | 46% overall, 100% on ai_analyzer.py |
| Tests passing | 6/6 (5 unit + 1 integration) |
| Repos tested against | 3 |
| PRs analyzed | 10 |
| Azure resources deployed | 5 (Resource Group, Key Vault, ACR, Container Instances, Log Analytics) |
| Docker image | pranalyzeracr.azurecr.io/pr-risk-analyzer:v1 |
| CI/CD pipeline runtime | ~1 minute 12 seconds (build/push/deploy stage) |
| Terraform state | Remote, in Azure Blob Storage (shared local ↔ CI) |

## Resume Bullet (Final)

> "Built a Python CLI tool that uses the GitHub REST API and Claude API to classify open pull requests as LOW, MEDIUM, or HIGH risk and generate plain-English summaries to support secure software development reviews, validated against 10 PRs across 3 open-source repos. Containerized with Docker, provisioned Azure infrastructure (Resource Group, Key Vault, Container Registry, Container Instances, Log Analytics) via Terraform IaC with remote state, and implemented a CI/CD pipeline in GitHub Actions that automatically tests, applies infrastructure changes, builds, pushes to ACR, and deploys on every push — with secrets managed through Azure Key Vault and 46% test coverage including 100% on core risk-analysis logic."

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

### `load_dotenv()` — Where It Lives Matters
> 📅 Refactor Sprint

`load_dotenv()` should only be called once, in the entrypoint (`analyze.py`) — not in modules that get imported.

**Why it works:**
If `ai_analyzer.py` and `github_client.py` both call `load_dotenv()` at import time, secrets may not be loaded yet when a container starts (no `.env` file in production). Moving it to `analyze.py` guarantees secrets are loaded before any module needs them.

**Good to know:**
In production (Azure Container Instances), there is no `.env` file. Secrets come from Azure Key Vault or environment variables passed at runtime via `--env-file` or Terraform variables.

---

### API Client Creation — Call Time vs Import Time
> 📅 Refactor Sprint

Create API clients inside functions, not at module import time.

**Why it works:**
Creating `anthropic.Anthropic()` at import time means the entire tool crashes immediately if the API key is missing. Creating it inside the function means the error happens when the function is called — at the right place, with the right context.

```python
# WRONG — crashes at import if key is missing
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# CORRECT — fails gracefully at call time
def analyze_pr_risk(pr_data):
    from anthropic import Anthropic
    client = Anthropic()
    ...
```

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
| `409` | Conflict | Resource already exists (seen in Terraform/Docker Hub) |
| `500` | Server error | Their problem, not yours |

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

---

# TESTING

> 📅 Weekend Sprint (pre-internship)

---

### Unit Tests vs Integration Tests
> 📅 Refactor Sprint ★

**Unit tests** (`test_analyzer.py`):
- Mock all dependencies (fake PR data)
- Fast — no API calls
- Test one function in isolation
- Always run on every commit

**Integration tests** (`test_ai_integration.py`):
- Call real services (Anthropic API)
- Slower — real API latency
- Test the full pipeline end-to-end
- Skipped unless `ANTHROPIC_API_KEY` is set
- Marked with `@pytest.mark.integration`

**Why the separation matters:**
Real teams run unit tests on every commit (fast, always pass). Integration tests run nightly or before deployment — they're the canary that says "does this actually work end-to-end?"

---

### pytest Markers
> 📅 Refactor Sprint

Markers let you run subsets of tests selectively.

```bash
pytest tests/ -m "not integration"  # unit tests only (fast)
pytest tests/test_ai_integration.py  # integration only
```

Register markers in `pytest.ini` to avoid warnings:
```ini
[pytest]
markers =
    integration: marks tests as integration (deselect with '-m "not integration"')
```

---

### Test Coverage
> 📅 Refactor Sprint

```bash
pip install pytest-cov
pytest --cov=analyzer --cov-report=term-missing
```

| Column | Meaning |
|---|---|
| Stmts | Total executable lines |
| Miss | Lines never executed by tests |
| Cover | Percentage of lines tests touched |
| Missing | Line numbers not covered |

**Current coverage:** 46% overall, 100% on `ai_analyzer.py` (core risk logic)

**Good to know:**
70–85% is defensible for a solo project. 100% coverage on the critical path (risk scoring) is the real win.

---

### Mock Data in Tests
> 📅 Weekend Sprint

Simulated inputs that mimic real API responses — used so tests run without actual API calls.

**Why it works:**
Real API calls in tests are slow, cost money, and can fail for external reasons. Mock data gives full control.

**Good to know:**
This is called "mocking" — standard practice in every professional codebase. The rule: unit tests should never touch the network.

---

---

# CI/CD & GITHUB ACTIONS

> 📅 Weekend Sprint → CI/CD Sprint → Infra Hardening Sprint

---

### What is CI/CD?
> 📅 Week 1 concept, implemented Weekend Sprint, extended CI/CD Sprint

**CI (Continuous Integration):** Automatically run tests every time code is pushed.
**CD (Continuous Delivery):** Automatically deploy when tests pass.

**Why it works:**
Manual deployments are slow, error-prone, and inconsistent. CI/CD pipelines run the same steps every time — catching bugs before they reach production.

---

### Full CI/CD Pipeline (Final State) ★
> 📅 Infra Hardening Sprint — final version

Every push to `main` triggers three jobs in sequence:

```
Job 1: Run Tests
    ↓ pytest -m "not integration" --cov
    ↓ tests pass

Job 2: Terraform Apply
    ↓ Login to Azure (Service Principal)
    ↓ Create Terraform remote state storage (idempotent)
    ↓ Grant SP Key Vault access via CLI (breaks chicken-and-egg)
    ↓ terraform init (connects to remote state)
    ↓ terraform import (existing resources — safe to no-op if already imported)
    ↓ terraform apply (creates/updates Log Analytics, access policy, container group)
    ↓ Logout of Azure

Job 3: Build, Push, Deploy
    ↓ Login to Azure (Service Principal)
    ↓ Login to ACR
    ↓ docker build
    ↓ docker push to ACR
    ↓ az container start (fresh run pulling latest image)
    ↓ Logout of Azure
```

**Key design decisions:**
- `needs: test` / `needs: terraform` — each job only runs if the previous one passes (fail fast, in order)
- `if: github.ref == 'refs/heads/main'` — infra/deploy jobs skip on PRs, only run on main
- `secure_environment_variables` — secrets never appear in logs
- `az logout` at end of every job — session cleaned up immediately
- Import step uses `set +e` and explicit `echo` markers per resource — makes debugging real failures possible instead of hiding all errors behind `2>/dev/null`

---

### Service Principal for CI/CD Authentication ★
> 📅 CI/CD Sprint

GitHub Actions authenticates to Azure using a Service Principal — not your personal account.

**Why it matters:**
- A `.edu` account can have conditional access policies that flag repeated/automated logins
- Service Principals are app identities with scoped permissions
- If the SP credentials are compromised, you revoke just the SP — not your whole account
- Every single Azure-touching step in the final pipeline uses `azure/login@v1` with `AZURE_CREDENTIALS` — the personal account is never contacted, anywhere in the pipeline

**Key mapping:**

| SP output field | GitHub Actions secret field |
|---|---|
| `appId` | `clientId` |
| `password` | `clientSecret` |
| `tenant` | `tenantId` |
| (known) | `subscriptionId` |

**Stored as:** `AZURE_CREDENTIALS` GitHub Actions secret in JSON format.

**Also usable as local env vars** (`ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID`) so Terraform can authenticate locally without `az login` at all — the professional pattern for local IaC development against enterprise subscriptions.

---

### `az container start` vs `az container restart`
> 📅 CI/CD Sprint

| Command | Use when |
|---|---|
| `az container restart` | Container is running or paused |
| `az container start` | Container is stopped (ExitCode 0, restart_policy = Never) |

**Why it matters:**
`restart` on a stopped container throws `ContainerGroupStopped` error. CLI tools with `restart_policy = "Never"` stop after completing — always use `start` to trigger a fresh run.

---

### GitHub Actions vs Azure Pipelines
> 📅 Weekend Sprint

| | GitHub Actions | Azure Pipelines |
|---|---|---|
| Where config lives | `.github/workflows/` | `azure-pipelines.yml` |
| Trigger | Push to GitHub | Push to Azure DevOps Repos |
| Your team uses | GitHub Actions (this project) | Azure Pipelines (internship) |

**Good to know:**
The concepts are identical — YAML config, triggered on push, runs steps in order. Your GitHub Actions experience maps directly to Azure Pipelines on day one.

---

---

# TERRAFORM & IAC

> 📅 Weekend Sprint → Azure Deploy Sprint → Infra Hardening Sprint

---

### What is Terraform?
> 📅 Weekend Sprint

An open-source Infrastructure as Code tool that lets you define cloud resources in configuration files and provision them automatically.

**Why it works:**
Instead of clicking through the Azure portal, you write `.tf` files describing what you want. Terraform figures out what to create, modify, or destroy.

**Good to know:**
Your manager specifically named Terraform as the team standard. The goal: environments should be buildable, tear-downable, and rebuildable via Terraform + automated pipelines.

---

### Core Terraform Commands
> 📅 Azure Deploy Sprint

| Command | What it does | When to use |
|---|---|---|
| `terraform init` | Downloads provider plugins, connects to backend | Once per project, or after changing providers/backend |
| `terraform plan` | Preview changes — no modifications made | Always before apply — like `git diff` before commit |
| `terraform apply` | Actually creates/modifies/destroys resources | After reviewing plan |
| `terraform destroy` | Tears down all resources | When done — saves money |
| `terraform destroy -target=resource` | Destroys one specific resource | When you need to recreate just one thing |
| `terraform import ADDRESS ID` | Brings an existing real resource into Terraform state | When a resource was created outside Terraform, or state was lost |
| `terraform state list` | Shows what resources Terraform is tracking | Debugging "no changes" surprises |

**★ Interview-ready answer:** `terraform plan` is safe — it just reads and compares. `terraform apply` is the one that costs money and makes changes.

---

### Terraform Remote State (Azure Blob Storage Backend) ★
> 📅 Infra Hardening Sprint

By default, `terraform.tfstate` lives only on the machine that ran `terraform apply`. That breaks the moment two different environments (your laptop and GitHub Actions) both need to manage the same infrastructure — each would think the other's resources don't exist and try to recreate them.

**The fix — a remote backend:**
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "pr-risk-analyzer-rg"
    storage_account_name = "pranalyzertfstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
```

**Why it works:**
State now lives in an Azure Storage Account blob, not on any one machine. Both your local terminal and GitHub Actions read/write the *same* state file, so `terraform plan` always reflects true reality regardless of where it's run from.

**Good to know:**
- The storage account itself has to exist before `terraform init` can use it as a backend — this is a classic bootstrapping problem, solved here by creating it via `az storage account create` as a pipeline step *before* `terraform init` runs
- State locking (via a lease on the blob) prevents two simultaneous `apply` runs from corrupting state — you'll see "Acquiring state lock" / "Releasing state lock" in the output

---

### `terraform import` — Bringing Existing Resources Under Management
> 📅 Infra Hardening Sprint ★

When infrastructure already exists in Azure but isn't in Terraform's state (e.g. it was created in an earlier run against local state, and CI is now using fresh remote state), `terraform apply` will try to create it again and Azure will reject it with "already exists."

**The fix:**
```bash
terraform import azurerm_resource_group.main \
  /subscriptions/<sub-id>/resourceGroups/pr-risk-analyzer-rg
```

**Resource ID formats differ per resource type** — most are the plain ARM resource ID, but composite resources like Key Vault access policies use a suffixed format:
```
/subscriptions/.../vaults/pr-analyzer-vault/objectId/<principal-object-id>
```

**Three possible outcomes when importing, all meaningful:**

| Result | Meaning |
|---|---|
| `Import successful!` | Resource existed in Azure but not in state — now it does |
| `Resource already managed by Terraform` | Already in state from a prior import — safe to ignore |
| `Cannot import non-existent remote object` | The resource doesn't actually exist in Azure (e.g. it was destroyed in a prior failed run) — safe to ignore, `apply` will create it fresh |

**Good to know:**
Wrap import commands in `set +e` in CI so one resource's "already imported" isn't treated as a pipeline failure — but keep the *actual* error output visible (don't blanket-suppress with `2>/dev/null`), or you'll hide real failures like a genuine permissions error and waste time debugging the wrong thing.

---

### The Chicken-and-Egg Problem: Data Sources vs Access Policies ★
> 📅 Infra Hardening Sprint — the trickiest bug of the whole project

**The setup:** `main.tf` had a `data "azurerm_key_vault_secret"` block to read secrets, and a `resource "azurerm_key_vault_access_policy"` to grant the Service Principal permission to read them. Both were defined in the same Terraform config.

**The problem:** *Any* Terraform command that loads the config — including `terraform import` for an unrelated resource — evaluates every `data` block up front. So even importing the Resource Group triggered a read of the Key Vault secrets, which failed with `403 Forbidden` because the access policy resource hadn't been *applied* yet. Terraform can't grant itself permission and use that permission in the same breath.

**The fix:** Grant the access policy via Azure CLI directly, *before* Terraform ever runs:
```bash
az keyvault set-policy \
  --name pr-analyzer-vault \
  --spn "<service-principal-client-id>" \
  --secret-permissions get list
```

Then let Terraform's `azurerm_key_vault_access_policy` resource `import` that same policy into state afterward, so Terraform "owns" it going forward without trying to recreate it.

**Why this pattern matters beyond this project:**
Any time Terraform needs to both grant an identity access *and* immediately use that access to read something (secrets, storage keys, etc.), you have a bootstrapping cycle. The general fix is always the same: grant access through an out-of-band step (CLI, portal, or a separate `apply -target`) first, then bring it under Terraform management.

---

### AWS → Azure Resource Mapping (for Terraform)
> 📅 Weekend Sprint

| AWS | Azure Terraform resource |
|---|---|
| AWS Account/Region scope | `azurerm_resource_group` |
| AWS Secrets Manager | `azurerm_key_vault` |
| ECS / Fargate | `azurerm_container_group` |
| ECR | `azurerm_container_registry` |
| IAM Role | `azurerm_role_assignment` |
| VPC | `azurerm_virtual_network` |
| CloudWatch Logs | `azurerm_log_analytics_workspace` |

---

### Container Group: CLI vs Web Service
> 📅 Azure Deploy Sprint

For CLI tools that run on demand (not web servers), use these settings:

```hcl
resource "azurerm_container_group" "analyzer" {
  ...
  ip_address_type = "None"      # no public endpoint — CLI tool, not a server
  restart_policy  = "Never"     # run once and stop cleanly (ExitCode 0)
  ...
}
```

**Why it works:**
- `"None"` avoids the `MissingIpAddressPorts` error Azure throws for public containers without exposed ports
- `"Never"` stops Azure from restarting the container after it finishes — which would cause infinite restart loops

---

### Key Vault Data Sources in Terraform
> 📅 CI/CD Sprint

Read secrets from Key Vault at deploy time using `data` blocks:

```hcl
data "azurerm_key_vault_secret" "anthropic_key" {
  name         = "anthropic-api-key"
  key_vault_id = azurerm_key_vault.main.id
}
```

Then reference in container:
```hcl
secure_environment_variables = {
  ANTHROPIC_API_KEY = data.azurerm_key_vault_secret.anthropic_key.value
}
```

**Why `secure_environment_variables` not `environment_variables`:**
Secure vars are redacted in all logs, portal output, and `terraform plan` output. Regular vars show in plain text.

**Gotcha (see Chicken-and-Egg entry above):** these `data` blocks are evaluated on *every* Terraform command that touches the config — not just `apply`. Permission to read them must exist before you run anything, including `import`.

---

### Azure Log Analytics Workspace
> 📅 Infra Hardening Sprint

Persistent, queryable storage for container logs — solves the "logs disappear when the container stops" problem.

```hcl
resource "azurerm_log_analytics_workspace" "main" {
  name                = "pr-analyzer-logs"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}
```

Wired into the container group via:
```hcl
diagnostics {
  log_analytics {
    workspace_id  = azurerm_log_analytics_workspace.main.workspace_id
    workspace_key = azurerm_log_analytics_workspace.main.primary_shared_key
  }
}
```

**AWS equivalent:** CloudWatch Logs.

**Status:** deployed and wired in; not yet manually verified end-to-end (Azure for Students log streaming had been unreliable via CLI/portal for this project) — but this is now the correct production pattern in place for any future debugging.

---

---

# AZURE

> 📅 Weekend Sprint → Azure Deploy Sprint → CI/CD Sprint → Infra Hardening Sprint

---

### AWS → Azure Concept Map
> 📅 Weekend Sprint

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
| CloudWatch Logs | Log Analytics Workspace |

---

### Azure Resource Hierarchy ★
> 📅 Azure Deploy Sprint

Know this cold for interviews:

```
Tenant (your org's Microsoft account)
  └── Subscription (billing boundary — your Azure for Students sub)
        └── Resource Group (logical container — pr-risk-analyzer-rg)
              ├── Key Vault (pr-analyzer-vault)
              ├── Container Registry (pranalyzeracr)
              ├── Container Instances (pr-risk-analyzer)
              ├── Log Analytics Workspace (pr-analyzer-logs)
              └── Storage Account (pranalyzertfstate — Terraform remote state)
```

**Why it matters:**
Thomas mentioned subscriptions constantly. Permissions, billing, and resource management all flow through this hierarchy.

---

### Azure Key Vault
> 📅 Azure Deploy Sprint + CI/CD Sprint + Infra Hardening Sprint ✅ Done

Azure's secrets management service — stores API keys, tokens, and passwords securely.

**Current state:** `ANTHROPIC_API_KEY` and `GITHUB_TOKEN` stored in Key Vault and injected into Container Instances at deploy time via Terraform `secure_environment_variables`. Service Principal access policy granted via CLI, then imported into Terraform state (see Chicken-and-Egg entry in Terraform section).

---

### Azure Container Registry (ACR)
> 📅 CI/CD Sprint ✅ Done

Private Docker image registry — stores your built images for Container Instances to pull.

**Current state:** `pranalyzeracr.azurecr.io/pr-risk-analyzer:v1` is live and being deployed automatically by GitHub Actions on every push.

**Good to know:** Azure for Students blocks `az acr build` (cloud-side builds, error `TasksOperationsNotAllowed`) — images must be built locally/in-CI and pushed with `docker push`, not built remotely by ACR.

---

### Azure Storage Account (Terraform Backend)
> 📅 Infra Hardening Sprint

A general-purpose Azure Storage Account, used here purely to hold the Terraform state blob — not application data.

**Why a separate concept from Blob Storage as "S3 equivalent":** the same service (Storage Account → Blob Container) is reused here for a DevOps purpose (state backend) rather than an application purpose (file storage). Same building block, different job.

---

### Docker Hub Rate Limits in Azure
> 📅 Azure Deploy Sprint

Azure Container Instances pulling from Docker Hub can hit 409 rate limit errors.

**Fix:** Use Microsoft Container Registry (MCR) instead:
```hcl
image = "mcr.microsoft.com/devcontainers/python:3.11"
```

**Why it works:**
MCR has no rate limits for Azure deployments. Real teams always pull base images from MCR when deploying to Azure.

---

---

# DOCKER

> 📅 Azure Deploy Sprint

---

### What is Docker?
> 📅 Azure Deploy Sprint

A tool that packages your application and all its dependencies into a container — a self-contained unit that runs identically anywhere.

**Why it works:**
Without Docker, "it works on my machine" is a constant problem. With Docker, the container is the machine — it runs the same on your laptop, in CI, and in Azure.

---

### Dockerfile
> 📅 Azure Deploy Sprint

```dockerfile
FROM python:3.11-slim          # start from Python 3.11 base image
WORKDIR /app                   # set working directory inside container
COPY requirements.txt .        # copy requirements first (layer caching)
RUN pip install --no-cache-dir -r requirements.txt  # install deps
COPY analyzer/ ./analyzer/     # copy source code
COPY analyze.py .              # copy entrypoint
ENTRYPOINT ["python", "analyze.py"]  # run this when container starts
```

**Why `requirements.txt` before code:**
Docker caches layers. Copying requirements first means pip only re-runs when requirements change — not on every code change.

---

### Key Docker Commands
> 📅 Azure Deploy Sprint + CI/CD Sprint

| Command | What it does |
|---|---|
| `docker build -t name:tag .` | Builds image from Dockerfile in current directory |
| `docker run --env-file .env name:tag --repo x/y` | Runs container with secrets from `.env` |
| `docker tag name:tag registry/name:tag` | Tags image for a specific registry |
| `docker push registry/name:tag` | Pushes image to a registry |
| `az acr login --name <acr>` | Authenticates Docker to push to ACR |

---

### Passing Secrets to Containers
> 📅 Azure Deploy Sprint + CI/CD Sprint

```bash
# Local development
docker run --env-file .env pr-risk-analyzer:v1 --repo owner/repo

# In Azure (via Terraform secure_environment_variables)
# Terraform reads from Key Vault and injects at deploy time
```

---

---

# SECURITY & SECRETS

> 📅 Week 1 → Refactor Sprint → CI/CD Sprint → Infra Hardening Sprint

---

### PAT Token vs Service Principal vs GitHub App ★
> 📅 CI/CD Sprint

| | PAT Token | Service Principal | GitHub App |
|---|---|---|---|
| Lifespan | Long-lived | Configurable | 1 hour (auto-rotated) |
| Scope | User-level | Subscription-level | Repo-level |
| Risk if exposed | High | Medium | Low |
| Used for | Local dev | CI/CD pipelines | Production GitHub auth |

**Current state:** Service Principal (`pr-risk-analyzer-sp`) used for every Azure interaction in the pipeline — local machine and CI both authenticate this way. Personal `.edu` account never used for automation.

---

### Secret Storage Progression
> 📅 CI/CD Sprint

| Where | Use case |
|---|---|
| `.env` file | Local development only — never commit |
| GitHub Actions secrets | CI/CD pipelines — `AZURE_CREDENTIALS`, `AZURE_TENANT_ID` live here |
| Azure Key Vault | Production runtime — `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` live here |

**Why this progression matters:**
Each layer adds security. `.env` → GitHub secrets → Key Vault mirrors how real teams mature their secret management.

---

### Never Paste Secrets in Chat ★
> 📅 CI/CD Sprint — learned the hard way

If a secret is ever posted publicly (chat, GitHub, Slack), treat it as compromised immediately:
1. Rotate it right away (`az ad sp credential reset` or generate a new client secret in the portal)
2. Check Azure activity logs for unauthorized use
3. Update any systems using the old secret (GitHub Actions secrets, local `.bashrc`, etc.)

**Why:** Secrets in chat logs, screenshots, or commit history are permanently exposed — even after deletion.

---

### Protecting a Personal/.edu Account During Automation Work ★
> 📅 Infra Hardening Sprint

When a personal account (especially a university-managed one) has conditional access policies, repeated `az login` calls during development can trigger security flags.

**The complete solution used in this project:**
- All local Terraform runs authenticate via `ARM_*` environment variables sourced from the Service Principal — never `az login` with the personal account
- All CI/CD runs authenticate via `azure/login@v1` using the same Service Principal, stored as a GitHub Actions secret
- The *only* place personal-account login would ever be needed is generating or rotating the Service Principal itself — and even that can be done through the Azure Portal UI instead of CLI if needed

**Why it matters:** this is the actual production pattern — engineers on real teams essentially never use their own identity for automated infrastructure work. Service Principals (or Managed Identities where possible) are the standard.

---

### `.gitignore` Non-Negotiables
> 📅 Week 1

```
.env
.venv/
terraform.tfvars
*.tfstate
*.tfstate.backup
.terraform/
reports/*.txt
.coverage
*.swp
```

---

---

# DEVOPS CONCEPTS

> 📅 Week 1–3 | Core internship focus

---

### Infrastructure as Code (IaC) ★
> 📅 Introduced Week 1, implemented and completed through Infra Hardening Sprint

The practice of managing and provisioning infrastructure through code rather than manual processes.

**Key benefits your manager named:**
- **Repeatability** — reduces drift and "it works on my machine" issues
- **Speed + safety** — faster recovery, lower blast radius when changes fail
- **Auditability** — clear history of what changed and why
- **Scale** — less manual toil, more time on reliability

**★ Interview answer:** "Terraform lets us build, tear down, and rebuild environments automatically. If something breaks, we run `terraform apply` and get back to a known good state in minutes. We keep state remote in Blob Storage so the pipeline and local dev both see the same reality."

---

### PR Risk Analysis
> 📅 Week 1–2

The practice of evaluating how risky a pull request is before merging it.

**Risk signals:**

| Signal | Risk implication |
|---|---|
| Auth/security files touched | High — regardless of line count |
| Many files changed | Wide blast radius |
| High additions, low deletions | Lots of new code, little cleanup |
| No description | Less reviewer context |
| Tests included | Lower risk |
| Draft PR | Not ready to merge |

---

---

# AI & PROMPT ENGINEERING

> 📅 Week 2

---

### The Three-Part Prompt Structure
> 📅 Week 2

1. **Role** — "You are a senior DevOps engineer" sets the reasoning perspective
2. **Format constraint** — JSON means you can parse the response programmatically
3. **Data** — the actual content Claude needs to make a judgment

---

### JSON Output Format
> 📅 Week 2

Always ask for JSON instead of plain text when building tools:

```python
"Respond ONLY with valid JSON: {\"risk_level\": \"HIGH\", \"summary\": \"...\"}"
result = json.loads(raw_response)
```

---

### Model Names in Anthropic API
> 📅 Refactor Sprint

Model names use **hyphens only** — no dots:
- ✅ `claude-haiku-4-5-20251001`
- ❌ `claude-haiku-4.5-20251001`

---

---

# HTTP & APIs

> 📅 Week 1–2

---

### HTTP Status Codes That Matter for This Project

| Code | Meaning | Where you saw it |
|---|---|---|
| `200` | OK | GitHub API success |
| `401` | Unauthorized | Expired/missing GitHub PAT |
| `403` | Forbidden | Token lacks scope; SP missing Key Vault access policy |
| `404` | Not found | Wrong repo, missing endpoint, wrong model name |
| `409` | Conflict | Docker Hub rate limit in Azure |

---

---

# ERRORS & FIXES

> 📅 Week 1 → Infra Hardening Sprint | Running log of every error encountered

---

### `error: externally-managed-environment`
- **Cause:** Ubuntu protects system Python from direct `pip install`
- **Fix:** Use a virtual environment

---

### `anthropic.NotFoundError: model: claude-haiku-4.5-20251001`
- **Cause:** Dots in model name instead of hyphens
- **Fix:** `claude-haiku-4-5-20251001` (all hyphens)

---

### `Terraform: Value for undeclared variable`
- **Cause:** Variable exists in `terraform.tfvars` but has no `variable` block in `main.tf`
- **Fix:** Add `variable "name" { description = "..." }` block to `main.tf`

---

### `MissingIpAddressPorts: ports in 'ipAddress' cannot be empty`
- **Cause:** `ip_address_type = "Public"` requires at least one port
- **Fix:** Set `ip_address_type = "None"` for CLI tools

---

### `409 Conflict: RegistryErrorResponse: error from docker registry`
- **Cause:** Docker Hub rate limiting Azure's pull request
- **Fix:** Use `mcr.microsoft.com/devcontainers/python:3.11`

---

### `ContainerGroupStopped: Container Group is stopped`
> 📅 CI/CD Sprint
- **Cause:** `az container restart` used on a stopped container
- **Fix:** Use `az container start` instead

---

### `Login failed: Not all parameters are provided in 'creds'`
> 📅 CI/CD Sprint
- **Cause:** `AZURE_CREDENTIALS` secret had wrong field names (`appId` instead of `clientId`)
- **Fix:** Map fields correctly: `appId → clientId`, `password → clientSecret`, `tenant → tenantId`

---

### `TasksOperationsNotAllowed: ACR Tasks not permitted`
> 📅 CI/CD Sprint
- **Cause:** Azure for Students blocks `az acr build` (cloud-side builds)
- **Fix:** Build locally with `docker build`, tag with ACR URL, push with `docker push`

---

### `InternalServerError` on `az container logs`
> 📅 Azure Deploy Sprint
- **Cause:** Azure for Students subscription limitation on log streaming for terminated containers
- **Fix:** Verify tool works locally with same env vars; use ExitCode 0 + restart count 0 as proxy evidence; Log Analytics workspace now deployed for future runs

---

### `Error: A resource with the ID "..." already exists - needs to be imported`
> 📅 Infra Hardening Sprint
- **Cause:** Resource exists in Azure but not in Terraform's (now-remote) state — common the first time a new backend or a new CI environment runs against pre-existing infra
- **Fix:** `terraform import <resource_address> <azure_resource_id>` for each affected resource

---

### `Error: Resource already managed by Terraform`
> 📅 Infra Hardening Sprint
- **Cause:** Attempted to import a resource that's already in state from a prior successful import
- **Fix:** None needed — this is expected and safe on repeat pipeline runs; don't let it block the pipeline (`set +e` + explicit per-resource logging)

---

### `Error: Cannot import non-existent remote object`
> 📅 Infra Hardening Sprint
- **Cause:** Tried to import a resource that was destroyed in an earlier failed run and no longer exists in Azure
- **Fix:** None needed — `terraform apply` creates it fresh afterward

---

### `403 Forbidden: does not have secrets get permission on key vault` (during `terraform import`, not just `apply`)
> 📅 Infra Hardening Sprint — the trickiest bug of the project ★
- **Cause:** `data "azurerm_key_vault_secret"` blocks are evaluated on *every* Terraform command that loads the config, including `import` for unrelated resources — the Service Principal didn't have Key Vault access yet because the access-granting resource hadn't been applied
- **Fix:** Grant access via `az keyvault set-policy --spn <client-id> --secret-permissions get list` directly through the CLI *before* any Terraform command runs, then import that policy into Terraform state afterward. See full write-up in the Terraform section.

---

### `argument --password/-p: expected one argument` (az login --service-principal)
> 📅 Infra Hardening Sprint
- **Cause:** Client secret value starts with a special character (e.g. `-`) or contains characters the shell interprets
- **Fix:** Write the secret to a temp file and pass with `--password @/path/to/file`, then delete the file immediately after

---

### `AADSTS7000215: Invalid client secret provided`
> 📅 Infra Hardening Sprint
- **Cause:** Used the secret **ID** (visible in the portal's list view) instead of the secret **value** (only shown once, at creation time)
- **Fix:** Generate a new client secret in Certificates & Secrets and copy the **Value** column immediately

---

### `docker: command not found` in WSL2
> 📅 Azure Deploy Sprint
- **Cause:** Docker not installed in WSL2 Ubuntu
- **Fix:** `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

---

---

# CHECKPOINTS

---

## Week 1 — Environment & GitHub Client ✅

| Question | Your Answer | Verdict |
|---|---|---|
| What does `load_dotenv()` do? | Reads the .env file and loads values so `os.getenv()` can access them | ✅ |
| What does `raise_for_status()` do? | Raises an error immediately if the request returned 4xx or 5xx | ✅ |
| What is a virtual environment? | Isolates project packages from the system Python | ✅ |

---

## Week 2 — AI Integration ✅

| Question | Your Answer | Verdict |
|---|---|---|
| Why send filenames to Claude, not just line counts? | Filenames tell Claude what kind of code changed — auth files are riskier than docs | ✅ |
| Why ask Claude for JSON instead of plain text? | So we can reliably parse the response with `json.loads()` | ✅ |

---

## Weekend Sprint — Tests, CI, Terraform ✅

| Question | Your Answer | Verdict |
|---|---|---|
| What is mock data and why use it in tests? | Simulates GitHub API responses so tests run without real API calls | ✅ |
| What does `terraform plan` do before `terraform apply`? | Previews changes without making them — like git diff before committing | ✅ |
| Why `ip_address_type = "None"` for a CLI tool? | CLI tools don't serve HTTP — no public endpoint needed | ✅ |
| Why pull from MCR instead of Docker Hub in Azure? | Docker Hub rate limits cause 409 errors — MCR has no limits | ✅ |

---

## CI/CD Sprint ✅

| Question | Your Answer | Verdict |
|---|---|---|
| Why does `needs: test` matter in the pipeline? | Deploy job only runs if tests pass — fail fast principle | ✅ |
| Why use a Service Principal instead of az login? | Protects .edu account from conditional access triggers; scoped app identity | ✅ |
| Why `az container start` not `az container restart`? | restart fails on stopped containers; start works regardless of state | ✅ |
| Why use `secure_environment_variables`? | Values are redacted in all logs and portal output | ✅ |

---

## Infra Hardening Sprint ✅

Final sprint — remote state, Log Analytics, and the Key Vault chicken-and-egg problem.

**Key lesson demonstrated:** Terraform `data` blocks are evaluated on every command that loads the config, not just `apply` — so an identity needing to both read secrets AND be granted permission to read them in the same config creates a bootstrapping cycle that has to be broken with an out-of-band step.

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
- [ ] What is the difference between Azure Pipelines and GitHub Actions YAML syntax?
- [ ] What is Azure RBAC and how does least privilege work in Azure?
- [ ] How does `DefaultAzureCredential` work and what auth methods does it try?
- [ ] How does a GitHub App generate short-lived tokens compared to a PAT?
- [ ] What is `terraform destroy` and when should you run it?
- [ ] What is the difference between `restart_policy = "Never"` and `"Always"` in Azure Container Instances?
- [ ] How would you verify Log Analytics is actually receiving container logs (KQL query basics)?
- [ ] What other Azure resources commonly hit the same "grant access, then use access" bootstrapping problem as Key Vault (hint: storage account RBAC, managed identities)?
- [ ] What is a Managed Identity and how would it replace the Service Principal pattern used here if this ran natively inside Azure (e.g. from an Azure DevOps agent)?

---

*Last updated: Infra Hardening Sprint ✅ | Project fully complete and closed out | Final pipeline verified green 2026-08-11*
