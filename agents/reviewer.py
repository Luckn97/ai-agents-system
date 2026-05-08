from typing import Any, Dict, List, Literal, TypedDict

from config import MAX_TOKENS, REVIEWER_MODEL, TEMPERATURE
from utils.llm import call_json_model
from utils.logger import get_logger

logger = get_logger(__name__)

Severity = Literal["low", "medium", "high"]


class BugFinding(TypedDict):
    severity: Severity
    issue: str
    fix: str


class ReviewResult(TypedDict):
    bugs: List[BugFinding]
    improvements: List[str]
    suggested_fixes: List[str]


REVIEWER_SYSTEM_PROMPT = """
You are a senior code reviewer.

You must respond with one strict JSON object and no additional text.
The JSON object must exactly match this schema:
{
  "bugs": [
    {
      "severity": "low|medium|high",
      "issue": "string describing the bug",
      "fix": "string describing the required fix"
    }
  ],
  "improvements": [],
  "suggested_fixes": []
}

Severity rules:
- high: correctness, security, data-loss, runtime failure, deployment failure, or broken requested functionality.
- medium: important maintainability, edge-case, performance, or reliability issue.
- low: minor clarity, style, or polish issue.

Rules:
- Return valid JSON only.
- Do not use markdown.
- Do not use triple backticks.
- Each improvements and suggested_fixes item must be a concise string.
- If there are no findings for a field, return an empty array for that field.
""".strip()

_VALID_SEVERITIES = {"low", "medium", "high"}


def _as_string_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []

    items: List[str] = []
    for item in value:
        if isinstance(item, dict):
            parts = [str(item.get(key, "")).strip() for key in ("issue", "fix", "description")]
            text = " | ".join(part for part in parts if part)
        else:
            text = str(item).strip()

def _normalize_severity(value: Any) -> Severity:
    severity = str(value or "medium").strip().lower()
    if severity not in _VALID_SEVERITIES:
        return "medium"
    return severity  # type: ignore[return-value]


def _normalize_bugs(value: Any) -> List[BugFinding]:
    if not isinstance(value, list):
        return []

    bugs: List[BugFinding] = []
    for item in value:
        if isinstance(item, dict):
            issue = str(item.get("issue", "")).strip()
            fix = str(item.get("fix", "")).strip()
            severity = _normalize_severity(item.get("severity", "medium"))
        else:
            issue = str(item).strip()
            fix = "Review and correct this issue."
            severity = "medium"

        if not issue:
            continue

        bugs.append(
            {
                "severity": severity,
                "issue": issue,
                "fix": fix,
            }
        )

    return bugs


def run_reviewer(code: str) -> ReviewResult:
    logger.info("Running reviewer agent")

    return items


def _normalize_review_response(response: Dict[str, Any]) -> ReviewResult:
    return {
        "bugs": _normalize_bugs(response.get("bugs", [])),
        "improvements": _as_string_list(response.get("improvements", [])),
        "suggested_fixes": _as_string_list(response.get("suggested_fixes", [])),
    }


async def run_reviewer_async(code: str) -> ReviewResult:
    logger.info("Running reviewer agent")

    user_prompt = f"Review this code:\n\n{code.strip()}"

    try:
        response: Dict[str, Any] = await asyncio.to_thread(
            call_json_model,
            model=REVIEWER_MODEL,
            system_prompt=REVIEWER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    except Exception:
        logger.exception("Reviewer agent failed")
        raise

    return _normalize_review_response(response)


def run_reviewer(code: str) -> ReviewResult:
    return asyncio.run(run_reviewer_async(code))
