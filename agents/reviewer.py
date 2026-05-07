import asyncio
from typing import Any, Dict, List, TypedDict

from config import MAX_TOKENS, REVIEWER_MODEL, TEMPERATURE
from utils.llm import call_json_model
from utils.logger import get_logger

logger = get_logger(__name__)


class ReviewResult(TypedDict):
    bugs: List[str]
    improvements: List[str]
    suggested_fixes: List[str]


REVIEWER_SYSTEM_PROMPT = """
You are a senior code reviewer.

You must respond with one strict JSON object and no additional text.
The JSON object must exactly match this schema:
{
  "bugs": [],
  "improvements": [],
  "suggested_fixes": []
}

Rules:
- Return valid JSON only.
- Do not use markdown.
- Do not use triple backticks.
- Each array must contain concise strings.
- bugs must contain correctness, security, runtime, deployment, or broken-functionality issues.
- improvements must contain maintainability, readability, edge-case, reliability, or performance improvements.
- suggested_fixes must contain concrete changes the coder can apply.
- If there are no findings for a field, return an empty array for that field.
""".strip()


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

        if text:
            items.append(text)

    return items


def _normalize_review_response(response: Dict[str, Any]) -> ReviewResult:
    return {
        "bugs": _as_string_list(response.get("bugs", [])),
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
