from typing import Any, Dict, List

from config import MAX_TOKENS, REVIEWER_MODEL, TEMPERATURE
from utils.llm import call_json_model
from utils.logger import get_logger

logger = get_logger(__name__)

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
- If there are no findings for a field, return an empty array for that field.
""".strip()


def _as_string_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def run_reviewer(code: str) -> Dict[str, List[str]]:
    logger.info("Running reviewer agent")

    user_prompt = f"Review this code:\n\n{code.strip()}"

    response: Dict[str, Any] = call_json_model(
        model=REVIEWER_MODEL,
        system_prompt=REVIEWER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    return {
        "bugs": _as_string_list(response.get("bugs", [])),
        "improvements": _as_string_list(response.get("improvements", [])),
        "suggested_fixes": _as_string_list(response.get("suggested_fixes", [])),
    }
