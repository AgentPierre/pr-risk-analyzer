# PR Risk Analyzer — Learning Notes
> This file is automatically updated by Claude after every checkpoint and learning moment.
> Last updated: Week 1

---

## The Learning Contract
Before running any code, be able to answer:
1. What does this do?
2. Why is it structured this way?
3. What would break if I removed or changed X?

---

## Environment Setup

### WSL2
- Runs a real Linux environment inside Windows
- All Linux/DevOps commands work natively inside it
- `wsl` is a **Windows-only command** — only run it in PowerShell, never in the Ubuntu terminal

### VS Code + WSL
- Open a project connected to WSL: run `code .` from the Ubuntu terminal
- Open integrated terminal: **Ctrl + `** (backtick, key above Tab)
- If terminal shows PowerShell instead of bash, switch via the dropdown `+` arrow

### Resetting a forgotten WSL password
```bash
# In PowerShell (not Ubuntu):
wsl -u root

# Then inside the Ubuntu root session:
passwd yourusername

# Then exit root:
exit
```

---

## Project Setup

### Terminal Commands Used
| Command | What it does |
|---|---|
| `cd ~` | Go to home directory (`~` always means home) |
| `mkdir foldername` | Create a new directory |
| `cd foldername` | Move into a directory |
| `pwd` | Print current directory (confirm where you are) |
| `touch filename` | Create an empty file |
| `find . -not -path './.git/*'` | List all project files excluding Git internals |
| `git init` | Initialize a Git repository in the current folder |

### nano (terminal text editor)
- Open a file: `nano filename`
- Save: `Ctrl + O` → Enter
- Exit: `Ctrl + X`

---

## Python Concepts

### `import` vs `from x import y`
- `import requests` — brings in the entire `requests` library
- `import os` — brings in the entire `os` (operating system) library
- `from dotenv import load_dotenv` — reaches into the `dotenv` library and pulls out **only** the `load_dotenv` function
- Think of it like a toolbox: `import` carries the whole box, `from x import y` grabs just the screwdriver

### `load_dotenv()`
- Reads your `.env` file and loads its values into the environment
- Must be called before `os.getenv()` — otherwise your environment variables won't exist yet
- Without it, `os.getenv("GITHUB_TOKEN")` would return `None`

### `os.getenv("KEY")`
- Retrieves a value from the environment by its name
- Returns `None` if the key doesn't exist — always verify it loaded

### `raise_for_status()`
- Called on an HTTP response object after making an API request
- Raises an error immediately if the status code is 4xx or 5xx
- Without it, your code silently continues even if the request failed
- Think of it as a bouncer: nothing gets through unless the request was clean
- Common status codes:
  - `200` — success
  - `401` — unauthorized (bad or missing token)
  - `404` — not found (wrong URL or repo doesn't exist)
  - `500` — server error (GitHub's problem, not yours)

### List Comprehension
```python
# Long version:
filenames = []
for f in files:
    filenames.append(f["filename"])

# Short version (list comprehension):
filenames = [f["filename"] for f in files]
```
- Builds a new list by looping in one line
- Pattern: `[expression for item in iterable]`

### Generator Expression
```python
# Long version:
total = 0
for f in files:
    total += f["additions"]

# Short version (generator expression):
total = sum(f["additions"] for f in files)
```
- Same idea as list comprehension but computes a single value instead of building a list
- Used inside functions like `sum()`, `max()`, `min()`

### HTTP Headers
- Sent with every API request to identify who is asking and what format you want back
- **Not CORS** — CORS is a browser security concept, not relevant in Python scripts
- In this project:
  - `Authorization: Bearer <token>` — proves you have permission (like showing an ID at the door)
  - `Accept: application/vnd.github+json` — tells GitHub to send the response in its JSON format

---

## Virtual Environments

### What it is
- An isolated Python installation just for your project
- Packages installed inside it don't affect the system Python or other projects
- Think of system Python as a shared kitchen, and the venv as your own private kitchen

### Why we needed it
- Newer Ubuntu versions protect system Python from direct `pip install` commands
- Using a venv is standard practice in all real Python projects anyway

### Commands
```bash
# Create the venv (only once):
python3 -m venv .venv

# Activate it (every time you open a new terminal):
source .venv/bin/activate

# You'll know it's active when you see (.venv) in your prompt

# Install packages:
pip install -r requirements.txt
```

### `source .venv/bin/activate` — what it actually does
- `source` runs a script in your **current shell session**
- The `activate` script rewires your terminal so `python` and `pip` point to the venv's versions
- Without `source`, activation would run in a subprocess and immediately disappear

### `pip` vs `pip3`
- `pip3` clarifies "use pip for Python 3" when both Python 2 and 3 are installed on the same system
- Inside a venv there's only one Python — plain `pip` works, no number needed

---

## Secrets Management

### `.env` file
- Stores sensitive values (API tokens) as named variables
- Never hardcoded in source files — pushing a token to GitHub means anyone can use it
- Format: `GITHUB_TOKEN=your_token_here`

### `.gitignore` file
- Tells Git to completely ignore certain files — never tracked, staged, or committed
```
.env
__pycache__/
*.pyc
.venv/
```

### GitHub Personal Access Token (PAT)
- Required because GitHub disabled plain password auth for API calls in 2021
- Set scope to `repo` for this project
- **Copy it immediately after generating — GitHub only shows it once**

---

## Errors & Fixes

### `error: externally-managed-environment`
- **Cause:** Newer Ubuntu protects system Python from direct `pip install`
- **Fix:** Create and activate a venv first
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### `wsl: command not found`
- **Cause:** Ran a Windows command inside the Ubuntu terminal
- **Fix:** Open PowerShell and run it there — `wsl` only works on Windows

### `bash: /path/to/folder: Is a directory`
- **Cause:** Typed a folder path as a command without `cd` in front
- **Fix:** `cd /home/perry/Projects/pr-risk-analyzer`

### `bash: .venv/bin/activate: No such file or directory`
- **Cause:** Tried to activate the venv from the wrong directory
- **Fix:** Navigate into the project folder first, then activate

---

## Checkpoints

### Week 1 — Environment & GitHub Client

| Question | Your Answer | Verdict |
|---|---|---|
| What does `load_dotenv()` do? | Reads the .env file and loads values into the environment so `os.getenv()` can access them | ✅ Correct |
| What does `raise_for_status()` do? | Raises an error immediately if the API request returned a 4xx or 5xx status code | ✅ Correct |
| What is a generator expression? | A compact way to loop and compute a value in one line | ✅ Correct |
| What is a virtual environment? | Isolates project packages from the system Python | ✅ Correct |
| What does `source .venv/bin/activate` do? | Activates the virtual environment from the source of the folder | 🟡 Half right — `source` runs the script in your current shell so the changes stick |
| Why `pip` not `pip3` inside a venv? | pip is the default syntax for a virtual environment | 🟡 Close — only one Python exists inside a venv so the `3` suffix is unnecessary |
| What do the three `import` lines do? | `requests` = HTTP library, `os` = OS tools, `from dotenv import load_dotenv` = grab one function from dotenv | ✅ Mostly correct |
| What is `HEADERS` and why send it? | CORS to accept the GitHub token request | 🟡 Wrong concept — CORS is browser-only. `HEADERS` identifies your script to GitHub via token + tells it what format to use |
| What is `[f["filename"] for f in files]`? | Finds the filenames in the list called files | ✅ Correct — this pattern is called a list comprehension |

---

## Questions to Follow Up On
- How does `raise_for_status()` decide what counts as an error? (hint: look up HTTP status code ranges)
- What other HTTP headers are commonly used in real APIs?
- What is the difference between a `GET` and a `POST` request?
- Why does GitHub's API use `Bearer` tokens instead of just passing the token directly?
