import json
from typing import Dict, List

from config import REVIEWER_MODEL
from utils.openai_client import call_openai

reviewer_prompt = (
    "You are a strict code reviewer. "
    "Return valid JSON only with keys: bugs, improvements, suggested_fixes. "
    "All values must be arrays of strings."
)

EMPTY_REVIEW: Dict[str, List[str]] = {
    "bugs": [],
    "improvements": [],
    "suggested_fixes": [],
}


def run_reviewer(code_text: str) -> Dict[str, List[str]]:
    user_prompt = (
        "Review the following code and return JSON only:\n\n"
        f"{code_text}\n\n"
        "Schema:\n"
        '{"bugs": [], "improvements": [], "suggested_fixes": []}'
    )
    raw = call_openai(REVIEWER_MODEL, reviewer_prompt, user_prompt, temperature=0.1)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return EMPTY_REVIEW.copy()

    normalized: Dict[str, List[str]] = {
        "bugs": parsed.get("bugs", []),
        "improvements": parsed.get("improvements", []),
        "suggested_fixes": parsed.get("suggested_fixes", []),
    }

    for key, value in normalized.items():
        if not isinstance(value, list):
            normalized[key] = [str(value)]
        else:
            normalized[key] = [str(v) for v in value]

    return normalized
