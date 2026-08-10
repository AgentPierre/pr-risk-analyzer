import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# create the Anthropic client using the API key from .env
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def analyze_pr_risk(parsed_pr: dict) -> dict:
    # format the PR data into a prompt Claude can reason about
    prompt = f"""You are a senior DevOps engineer reviewing a pull request.
Analyze this PR and respond with ONLY a JSON object in this exact format:
{{"risk_level": "LOW" or "MEDIUM" or "HIGH", "summary": "2-3 sentence summary of the changes and why you rated the risk this way"}}

PR Details:
- Title: {parsed_pr['title']}
- Author: {parsed_pr['author']}
- Description: {parsed_pr['description']}
- Files changed: {parsed_pr['files_changed']}
- Additions: {parsed_pr['additions']}
- Deletions: {parsed_pr['deletions']}
- Files touched: {', '.join(parsed_pr['filenames'][:10])}
"""

    # send the prompt to Claude and get a response
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )

    # extract the text response from Claude's reply
    raw = message.content[0].text

    # strip markdown code fences if Claude wrapped the JSON in them
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    # parse the cleaned JSON into a Python dict
    import json
    result = json.loads(raw)

    return result
