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
    # Allow selecting model via environment (default to haiku series)
    model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")

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

    # Call the API with error handling to give clearer diagnostics
    try:
        message = client.messages.create(
            model=model,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        # Best-effort classification of common auth/model errors so the
        # user gets actionable guidance rather than a raw stacktrace.
        msg = str(e).lower()
        if "authentication" in msg or "invalid api key" in msg or "401" in msg:
            raise RuntimeError(
                "Anthropic authentication failed: API key is invalid or revoked. "
                "Verify `ANTHROPIC_API_KEY` and ensure it has access to the requested model."
            ) from e
        if "model" in msg or "no such model" in msg or "not found" in msg:
            raise RuntimeError(
                f"Model error when calling Anthropic: {e}. Try setting ANTHROPIC_MODEL to a model you have access to."
            ) from e
        raise

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
