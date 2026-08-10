---
description: "Draft a git commit message from the current changes, then commit and push after approval"
argument-hint: "Optional notes about the change or constraints"
agent: "agent"
---
Review the current worktree and prepare a commit for the user's changes.

Follow this flow:

1. Inspect the current `git status` and diff.
2. Summarize the changes briefly and call out anything unusual or unrelated.
3. Draft a concise commit subject in imperative mood, plus an optional body if the changes need context.
4. Ask for explicit approval before making any git changes.
5. After approval, stage the intended files, create the commit, and push the current branch to its upstream.
6. If there is no upstream, the push fails, or the tree contains unexpected unrelated changes, explain that clearly and stop.

Keep the commit message grounded in the actual diff. Do not invent changes, and do not commit or push before approval.