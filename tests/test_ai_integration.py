import os

import pytest

from analyzer.ai_analyzer import analyze_pr_risk


LIVE_PR_SAMPLE = {
    "title": "Refactor risk scoring prompt",
    "author": "copilot",
    "description": "Updates the analyzer prompt and validation path for clearer risk summaries.",
    "files_changed": 2,
    "additions": 18,
    "deletions": 6,
    "filenames": ["analyzer/ai_analyzer.py", "tests/test_ai_integration.py"],
}


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="Set ANTHROPIC_API_KEY to run the live integration test.",
)
def test_analyze_pr_risk_with_real_api():
    result = analyze_pr_risk(LIVE_PR_SAMPLE)

    assert result["risk_level"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(result["summary"], str)
    assert result["summary"].strip()