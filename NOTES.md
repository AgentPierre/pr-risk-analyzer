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

> 📅 Week 1–2

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

# DEVOPS CONCEPTS

> 📅 Week 1–3 | Core internship focus

---

### Infrastructure as Code (IaC)
> 📅 Introduced Week 1 — deep dive coming

The practice of managing and provisioning infrastructure through code rather than manual processes.

**Why it works:**
Code is repeatable, versionable, and auditable. A Terraform file that defines a server can be run 100 times and produce the same result — a human clicking through a console cannot guarantee that.

**Good to know:**
Your manager specifically named Terraform + automated pipelines as the team standard. The goal: environments should be buildable, tear-downable, and rebuildable automatically.

Key benefits:
- **Repeatability** — reduces "it works on my machine" drift
- **Speed + safety** — faster recovery, lower blast radius when changes fail
- **Auditability** — clear history of what changed and why
- **Scale** — less manual toil, more time on reliability

---

### CI/CD (Continuous Integration / Continuous Delivery)
> 📅 Introduced Week 1 — deep dive coming

Automation pipelines that build, test, and deploy code every time a change is pushed.

**Why it works:**
Manual deployments are slow, error-prone, and inconsistent. CI/CD pipelines run the same steps every time — catching bugs before they reach production.

**Good to know:**
CI = automated testing on every commit. CD = automated deployment when tests pass. Your manager's team uses this as the backbone of their cloud operations.

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

$5 in credits ≈ 5,000–10,000 risk analysis calls at current pricing.

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
CORS is a browser security concept — it does NOT apply to Python scripts. Common headers in DevOps tooling:

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
On real teams, production secrets live in AWS Secrets Manager, HashiCorp Vault, or GitHub Actions secrets — never `.env` files.

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

> 📅 Week 1–3 | Add every new error you encounter

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
  or enter path: `/home/perry/Projects/pr-risk-analyzer/.venv/bin/python`

---

### `json.decoder.JSONDecodeError: Expecting value`
> 📅 Week 2

- **Cause:** Claude wrapped JSON response in markdown code fences
- **Fix:** Strip code fences before `json.loads()`
```python
raw = raw.strip()
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()
```

---

### `anthropic.BadRequestError: credit balance too low`
> 📅 Week 2

- **Cause:** No credits on Anthropic account
- **Fix:** console.anthropic.com → Plans & Billing → add credits ($5 covers this project)

---

---

# CHECKPOINTS

---

## Week 1 — Environment & GitHub Client
> 📅 Week 1

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
> 📅 Week 2

| Question | Your Answer | Verdict |
|---|---|---|
| Why send filenames to Claude, not just line counts? | Because filenames tell Claude what kind of code changed — auth files are riskier than docs | ✅ Correct |
| Why ask Claude for JSON instead of plain text? | So we can reliably parse the response with `json.loads()` and extract specific fields | ✅ Correct |
| Why does per-call API cost matter? | At scale, small per-call costs add up — real teams monitor and optimize AI API spend | ✅ Correct |

---

## Week 3 — CLI Polish
> 📅 Week 3 — in progress

| Question | Your Answer | Verdict |
|---|---|---|
| What happens if you run without --limit? | Uses default value of 5, analyzes first 5 PRs | ✅ Correct |
| Why use `with open()` instead of plain `open()`? | `with` automatically closes the file when the block ends, even if an error occurs | ✅ Correct |

---

---

# QUESTIONS TO FOLLOW UP ON

> Review these before your internship starts

- [ ] What is the difference between a `GET` and a `POST` request?
- [ ] Why does GitHub's API use `Bearer` tokens instead of passing the token directly?
- [ ] What happens to your Git history if you commit a secret by accident?
- [ ] What is `git diff` and when would you use it?
- [ ] What is token length and how does it affect AI API cost?
- [ ] How would you cache AI responses to avoid paying for the same PR twice?
- [ ] What is Terraform and how does `terraform apply` work?
- [ ] What is a CI/CD pipeline and what triggers it?
- [ ] What is Docker and why do teams containerize applications?

---

*Last updated: Week 3 in progress*
