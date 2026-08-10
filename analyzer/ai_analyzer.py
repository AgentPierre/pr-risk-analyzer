import os
import json
from typing import Dict

try:
    import anthropic
except Exception:  # pragma: no cover - dependency missing
    anthropic = None


def analyze_pr_risk(parsed_pr: dict) -> Dict[str, str]:
    """Analyze a parsed PR using Anthropic Claude and return a typed dict.

    The Anthropic client is created at call time so missing API keys do not
    cause import-time failures. Expects ANTHROPIC_API_KEY to be set in the
    environment (loaded by the application entrypoint).
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in the environment")
    if anthropic is None:
        raise RuntimeError("anthropic package is not installed")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = (
        f"You are a senior DevOps engineer reviewing a pull request.\n"
        f"Analyze this PR and respond with ONLY a JSON object in this exact format:\n"
        f"{{\"risk_level\": \"LOW\" or \"MEDIUM\" or \"HIGH\", \"summary\": \"2-3 sentence summary\"}}\n\n"
        f"PR Details:\n"
        f"- Title: {parsed_pr.get('title')}\n"
        f"- Author: {parsed_pr.get('author')}\n"
        f"- Description: {parsed_pr.get('description')}\n"
        f"- Files changed: {parsed_pr.get('files_changed')}\n"
        f"- Additions: {parsed_pr.get('additions')}\n"
        f"- Deletions: {parsed_pr.get('deletions')}\n"
        f"- Files touched: {', '.join(parsed_pr.get('filenames', [])[:10])}\n"
    )

    # Call the API
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract text response safely
    raw = ""
    try:
        raw = message.content[0].text
    except Exception:
        # best-effort: try str(message)
        raw = str(message)

    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 2:
            raw = parts[1]
            if raw.startswith("json"):
                raw = raw[4:]
    raw = raw.strip()

    try:
        result = json.loads(raw)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from model response: {e}; raw={raw}")

    return result
