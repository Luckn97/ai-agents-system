import json
from typing import Dict, List

from utils.openai_client import call_openai

reviewer_prompt = (
    "You are a strict code reviewer. "
    "Always return valid JSON with exactly these keys: bugs, improvements, suggested_fixes. "
    "Each value must be an array of strings."
)


EMPTY_REVIEW: Dict[str, List[str]] = {
    "bugs": [],
    "improvements": [],
    "suggested_fixes": [],
}


def run_reviewer(code_text: str) -> Dict[str, List[str]]:
    user_prompt = (
        "Review the following code and return only JSON:\n\n"
        f"{code_text}\n\n"
        "Required format:\n"
        '{"bugs": [], "improvements": [], "suggested_fixes": []}'
    )
    raw = call_openai(reviewer_prompt, user_prompt, temperature=0.1)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return EMPTY_REVIEW.copy()

    normalized = {
        "bugs": parsed.get("bugs", []),
        "improvements": parsed.get("improvements", []),
        "suggested_fixes": parsed.get("suggested_fixes", []),
    }

    for key, value in normalized.items():
        if not isinstance(value, list):
            normalized[key] = [str(value)]
        else:
            normalized[key] = [str(item) for item in value]

    return normalized
