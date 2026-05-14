# PR Risk Analyzer — Learning Notes
> Automatically updated by Claude after every checkpoint and learning moment.
> Every concept includes "Why it works" and "Good to know" for future reference.
> Last updated: Week 1 complete

---

## The Learning Contract
Before running any code, be able to answer:
1. What does this do?
2. Why is it structured this way?
3. What would break if I removed or changed X?

---

## GIT

### What is Git?
A version control system that tracks every change you make to files over time.
Think of it as a save system for your code — except every save has a message, a timestamp, and can be rewound.

**Why it works:**
Git stores your project history as a chain of snapshots called commits. Each commit points to the previous one, forming a timeline. This means you can always go back to any point in that timeline, see what changed, and why.

**Good to know:**
Git is the industry standard. Every team you'll ever work on uses it. Your commit history is a professional artifact — future employers and teammates read it.

---

### `git init`
Initializes a new Git repository in the current folder.

**Why it works:**
Creates a hidden `.git` folder that stores your entire project history. Without it, Git has no idea your folder exists and none of the other Git commands will work.

**Good to know:**
You only ever run this once per project, at the very beginning. If you run it inside an existing repo by accident, it can cause issues — always check you're in the right folder first with `pwd`.

---

### `git status`
Shows the current state of your working directory — what's changed, what's staged, what's untracked.

**Why it works:**
Git tracks three zones:
- **Untracked** — new files Git hasn't seen before (shown in red)
- **Staged** — files you've told Git to include in the next commit (shown in green)
- **Modified** — files Git knows about that have changed since the last commit

**Good to know:**
Run `git status` constantly — before staging, before committing, after pulling. It's your sanity check. Real engineers run it more than almost any other command.

---

### `git add .`
Stages all changed and new files in the current folder for the next commit.

**Why it works:**
The `.` means "everything from here". Git reads your `.gitignore` first and silently skips any files listed there — so `.env` and `.venv/` are never staged even when you run `git add .`.

**Good to know:**
You can also stage individual files with `git add filename` if you only want to commit specific changes. This gives you fine-grained control over what goes into each commit — useful when you've made multiple unrelated changes.

---

### `git commit -m "message"`
Saves a snapshot of everything that's staged, with a descriptive message.

**Why it works:**
A commit is permanent (unless you explicitly undo it). It records who made the change, when, and why. The `-m` flag lets you write the message inline — without it, Git opens a text editor for you to write the message.

**Good to know:**
Use the **Conventional Commits** format — it's standard on real engineering teams:
- `feat:` — a new feature
- `fix:` — a bug fix
- `docs:` — documentation only
- `chore:` — maintenance (updating dependencies, config changes)
- `refactor:` — code restructure with no behavior change

Example: `git commit -m "feat: add GitHub API client with PR fetching"`

---

### Commit before you test — always
Stage and commit your working code before running or testing it.

**Why it works:**
If your test run reveals a bug and you make changes trying to fix it, you can always run `git diff` to see exactly what changed, or `git checkout .` to throw away your changes and go back to the last clean state.

**Good to know:**
This is the habit that separates developers who debug confidently from ones who get lost. Think of each commit as a checkpoint in a game — you can always reload from here.

---

## LINUX & TERMINAL

### The Terminal Mental Model
The terminal always has a "current location" — the folder you're working in right now. Every command runs relative to that location.

**Why it works:**
Unlike a GUI where you click into folders, the terminal requires you to navigate with commands. Your location affects everything — `git init` in the wrong folder, `pip install` outside a venv, or `touch` in the wrong directory all cause silent problems.

**Good to know:**
Always run `pwd` (print working directory) when something isn't behaving as expected. 90% of the time you're in the wrong folder.

---

### Key Navigation Commands

| Command | What it does | Why it works |
|---|---|---|
| `cd ~` | Go to home directory | `~` is a shell shortcut that always expands to your home path |
| `cd foldername` | Move into a folder | Changes your current working directory |
| `cd ..` | Go up one level | `..` always means "parent directory" in Linux |
| `pwd` | Print current directory | Stands for Print Working Directory — your GPS in the terminal |
| `mkdir foldername` | Create a new folder | Makes an empty directory at the specified path |
| `touch filename` | Create an empty file | Originally used to update file timestamps — now mainly used to create files |
| `ls` | List files in current folder | Short for "list" — shows what's in your current directory |
| `ls -la` | List all files including hidden | `-l` = long format, `-a` = all files (including dotfiles like `.env`) |
| `find . -not -path './.git/*'` | List all project files | Recursively lists everything, excluding Git internals |

---

### Hidden Files (dotfiles)
Files starting with `.` are hidden by default in Linux (e.g. `.env`, `.gitignore`, `.venv`).

**Why it works:**
Linux convention: a leading dot means "configuration or system file — don't show by default." This keeps directories clean and prevents accidental deletion.

**Good to know:**
Run `ls -la` to see hidden files. This matters a lot in DevOps — most config files are dotfiles (`.bashrc`, `.ssh/`, `.kube/config`).

---

### `source`
Runs a script in your **current shell session** rather than a subprocess.

**Why it works:**
Normally when you run a script, it runs in a child process and any changes it makes (like setting environment variables) disappear when it exits. `source` runs the script directly in your current shell so changes stick.

**Good to know:**
You'll use `source` in two main contexts in DevOps:
1. `source .venv/bin/activate` — activate a Python venv
2. `source ~/.bashrc` — reload your shell config after editing it

---

### nano (terminal text editor)
A simple text editor that runs inside the terminal.

| Action | Keys |
|---|---|
| Save | `Ctrl + O` → Enter |
| Exit | `Ctrl + X` |
| Search | `Ctrl + W` |

**Good to know:**
nano is great for quick edits. For bigger files, use VS Code (`code filename` from the terminal). More powerful terminal editors like `vim` exist — you'll encounter them on servers — but nano is fine for now.

---

## PYTHON

### Virtual Environments (venv)

**Why it works:**
Creates an isolated Python installation for your project. Packages installed inside it don't affect system Python or other projects. Newer Ubuntu versions enforce this by blocking direct `pip install` to protect system tools that depend on Python.

**Good to know:**
Every real Python project uses a venv. It's not optional on teams — it's how you guarantee "it works on my machine" actually means something.

```bash
python3 -m venv .venv          # create (once)
source .venv/bin/activate      # activate (every new terminal session)
pip install -r requirements.txt  # install packages
```

---

### `pip` vs `pip3`
- `pip3` clarifies "use pip for Python 3" when Python 2 and 3 are both installed
- Inside a venv there's only one Python — plain `pip` works

**Good to know:**
Python 2 reached end-of-life in 2020. Most modern systems only have Python 3, but the `pip3` convention stuck. Inside a venv you never need the `3` suffix.

---

### `import` vs `from x import y`
- `import requests` — brings in the whole library
- `from dotenv import load_dotenv` — grabs one specific function from a library

**Why it works:**
Both load code into your script, but `from x import y` is more surgical. It avoids polluting your namespace with everything in a library when you only need one function.

**Good to know:**
Use `from x import y` when you only need specific pieces of a library. Use `import x` when you need multiple things from it and want to call them as `x.something()`.

---

### `load_dotenv()`
Reads your `.env` file and loads its key-value pairs into the environment.

**Why it works:**
Python's `os.getenv()` reads from the process environment, not from files. `load_dotenv()` bridges the gap by reading the file and injecting its values into the environment before your code runs.

**Good to know:**
Call it at the top of your script before any `os.getenv()` calls. If you call it too late, your variables won't be available yet.

---

### `raise_for_status()`
Raises an exception if the HTTP response has an error status code (4xx or 5xx).

**Why it works:**
`requests.get()` succeeds as long as it gets *any* response — even a 404 or 401. Without `raise_for_status()` your code silently continues with bad data. With it, failures are loud and immediate.

**Good to know:**
Common status codes to know:
| Code | Meaning | Likely cause in this project |
|---|---|---|
| `200` | OK | Everything worked |
| `401` | Unauthorized | Bad or missing GitHub token |
| `403` | Forbidden | Token doesn't have repo scope |
| `404` | Not found | Wrong owner/repo name |
| `422` | Unprocessable | Malformed request parameters |
| `500` | Server error | GitHub's problem, not yours |

---

### `if __name__ == "__main__":`
The entry point guard — ensures `main()` only runs when the file is executed directly, not when it's imported by another file.

**Why it works:**
Python sets a special variable called `__name__` on every file it runs. When you run a file directly (`python3 analyze.py`), Python sets `__name__` to `"__main__"`. When a file is imported by another file, `__name__` becomes the filename instead. This one-line check is how Python tells the difference.

**Good to know:**
Without this guard, any file that imports `analyze.py` would immediately start fetching PRs — which you never want. As your project grows and files start importing each other, this guard prevents unintended side effects. You'll see it at the bottom of almost every Python script.

```python
# This only runs when you do: python3 analyze.py
# It does NOT run if another file does: import analyze
if __name__ == "__main__":
    main()
```

---

### List Comprehension
A compact way to build a new list by looping in one line.

```python
# Long version:
filenames = []
for f in files:
    filenames.append(f["filename"])

# List comprehension:
filenames = [f["filename"] for f in files]
```

**Why it works:**
Python evaluates the expression for each item and collects the results into a new list. It's not just syntax sugar — it's also faster than a for loop for list building.

**Good to know:**
Pattern: `[expression for item in iterable]`. You can also add a condition: `[f["filename"] for f in files if f["status"] != "removed"]`

---

### Generator Expression
Same idea as a list comprehension but computes a single value instead of building a list.

```python
total = sum(f["additions"] for f in files)
```

**Why it works:**
Instead of building an intermediate list and then summing it, a generator yields one value at a time and feeds it directly to `sum()`. More memory efficient for large datasets.

**Good to know:**
Use generator expressions inside `sum()`, `max()`, `min()`, `any()`, `all()`. If you need the actual list, use a list comprehension instead.

---

## HTTP & APIs

### HTTP Headers
Key-value pairs sent with every API request that describe who is asking and what they want.

**Why it works:**
The server reads headers to decide whether to accept the request and how to format the response. Without `Authorization`, GitHub returns 401. Without `Accept`, it may return a different JSON format.

**Good to know:**
CORS (Cross-Origin Resource Sharing) is a browser security concept — it does NOT apply to Python scripts. Headers in Python scripts are purely for API authentication and content negotiation.

Common headers you'll see in DevOps tooling:
| Header | Purpose |
|---|---|
| `Authorization: Bearer <token>` | Prove identity via token |
| `Accept: application/json` | Request JSON response format |
| `Content-Type: application/json` | Tell server you're sending JSON |
| `X-Request-ID` | Trace a request through distributed systems |

---

### GitHub Personal Access Token (PAT)
A token that grants API access to GitHub on your behalf.

**Why it works:**
GitHub disabled password authentication for API calls in 2021 — tokens are scoped (you control exactly what they can do) and revocable (delete without changing your password).

**Good to know:**
- Set the minimum scope needed — `repo` read access for this project
- Tokens expire — set a reminder to regenerate before your internship starts
- Never hardcode tokens in source files — always use `.env`
- If you accidentally commit a token, revoke it immediately and generate a new one

---

## SECRETS MANAGEMENT

### `.env` file
Stores sensitive values (tokens, passwords, API keys) as named variables outside of source code.

**Why it works:**
Your Python code reads values from the environment at runtime, not from the file directly. This means you can change secrets without touching code, and different environments (dev, staging, prod) can have different values.

**Good to know:**
`.env` is a local-only file — it never leaves your machine. On real teams, secrets in production are managed by tools like AWS Secrets Manager, HashiCorp Vault, or GitHub Actions secrets — never `.env` files.

---

### `.gitignore`
Tells Git which files and folders to never track, stage, or commit.

**Why it works:**
Git checks `.gitignore` before staging. Any matching file is silently skipped — even with `git add .`. This is your last line of defense against accidentally committing secrets.

**Good to know:**
Best practice: write your `.gitignore` before your first commit. If you commit a secret first and add it to `.gitignore` after, the secret is already in your Git history — you'd need to rewrite history to remove it.

---

## ERRORS & FIXES

### `error: externally-managed-environment`
- **Cause:** Newer Ubuntu protects system Python from direct `pip install`
- **Fix:** Use a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### `wsl: command not found`
- **Cause:** Ran a Windows-only command inside the Ubuntu terminal
- **Fix:** Open PowerShell and run it there

### `bash: /path/to/folder: Is a directory`
- **Cause:** Typed a folder path as a command — forgot `cd` in front
- **Fix:** `cd /home/perry/Projects/pr-risk-analyzer`

### `bash: .venv/bin/activate: No such file or directory`
- **Cause:** Tried to activate the venv from the wrong directory
- **Fix:** Navigate into the project folder first, then activate

### Git identity error on first commit
- **Cause:** Git doesn't know who you are yet
- **Fix:**
```bash
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

### `Command 'python' not found`
- **Cause:** Ubuntu only ships with `python3` — the `python` alias doesn't exist by default
- **Fix:** Always use `python3` to run scripts, or activate your venv first (which sets up the alias)
```bash
python3 analyze.py --repo owner/repo
```

### VS Code shows `Import "dotenv" could not be resolved`
- **Cause:** VS Code is pointing at system Python instead of your venv
- **Fix:** `Ctrl + Shift + P` → `Python: Select Interpreter` → select the `.venv` option
  or enter path manually: `/home/perry/Projects/pr-risk-analyzer/.venv/bin/python`

---

## CHECKPOINTS

### Week 1 — Environment & GitHub Client

| Question | Your Answer | Verdict |
|---|---|---|
| What does `load_dotenv()` do? | Reads the .env file and loads values into the environment so `os.getenv()` can access them | ✅ Correct |
| What does `raise_for_status()` do? | Raises an error immediately if the API request returned a 4xx or 5xx status code | ✅ Correct |
| What is a generator expression? | A compact way to loop and compute a value in one line | ✅ Correct |
| What is a virtual environment? | Isolates project packages from the system Python | ✅ Correct |
| What does `source .venv/bin/activate` do? | Activates the virtual environment from the source of the folder | 🟡 Half right — `source` runs it in your current shell so the changes stick |
| Why `pip` not `pip3` inside a venv? | pip is the default syntax for a virtual environment | 🟡 Close — only one Python exists inside a venv so the `3` suffix is unnecessary |
| What do the three `import` lines do? | `requests` = HTTP library, `os` = OS tools, `from dotenv import load_dotenv` = grab one function | ✅ Mostly correct |
| What is `HEADERS` and why send it? | CORS to accept the GitHub token request | 🟡 Wrong concept — CORS is browser-only. `HEADERS` proves identity + sets response format |
| What is `[f["filename"] for f in files]`? | Finds the filenames in the list called files | ✅ Correct — this is called a list comprehension |
| What does `if __name__ == "__main__":` do? | It's the entry point for the code | ✅ Correct — only runs `main()` when the file is executed directly, not when imported |

---

## QUESTIONS TO FOLLOW UP ON
- How does `raise_for_status()` decide what counts as an error? (hint: look up HTTP status code ranges)
- What other HTTP headers are commonly used in real APIs?
- What is the difference between a `GET` and a `POST` request?
- Why does GitHub's API use `Bearer` tokens instead of passing the token directly?
- What happens to your Git history if you commit a secret by accident?
- What is `git diff` and when would you use it?

---

## COMING UP
- Week 2: AI integration — pipe PR data into Claude API for risk ratings
- Week 3: CLI polish with argparse, export to report
- Week 4: pytest basics, clean commits, README
