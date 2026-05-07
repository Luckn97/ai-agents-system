import asyncio
import json
from typing import Any, Dict, Optional

from config import CODER_MODEL, MAX_TOKENS, TEMPERATURE
from utils.llm import call_json_model
from utils.logger import get_logger

logger = get_logger(__name__)

CODER_SYSTEM_PROMPT = """
You are a senior Python software engineer.

You must respond with one strict JSON object and no additional text.
The JSON object must exactly match this schema:
{
  "code": "string containing complete production-ready code",
  "rationale": "string containing a concise explanation of what changed"
}

Rules:
- Return valid JSON only.
- Do not use markdown.
- Do not use triple backticks.
- Always include complete, runnable code in the code field.
- Keep the implementation minimal, clean, and production-ready.
- Preserve existing behavior unless reviewer feedback requires a change.
- If reviewer_feedback is provided, improve the previous code, fix bugs, and apply suggested_fixes.
- You MUST fix all reviewer issues.
""".strip()


def _feedback_to_text(reviewer_feedback: Any) -> str:
    if reviewer_feedback is None or reviewer_feedback == "":
        return ""
    if isinstance(reviewer_feedback, str):
        return reviewer_feedback.strip()
    return json.dumps(reviewer_feedback, ensure_ascii=False)


def _normalize_coder_response(response: Dict[str, Any]) -> Dict[str, str]:
    return {
        "code": str(response.get("code", "")).strip(),
        "rationale": str(response.get("rationale", "")).strip(),
    }


async def run_coder_async(
    task: str,
    reviewer_feedback: Optional[Any] = None,
    previous_code: str = "",
    *,
    review_feedback: Optional[Any] = None,
) -> Dict[str, str]:
    logger.info("Running coder agent")

    feedback_text = _feedback_to_text(
        reviewer_feedback if reviewer_feedback is not None else review_feedback
    )
    user_prompt = f"Task:\n{task.strip()}"

    if previous_code:
        user_prompt += f"\n\nPrevious code to improve:\n{previous_code.strip()}"

    if feedback_text:
        user_prompt += (
            "\n\nreviewer_feedback:\n"
            f"{feedback_text}\n\n"
            "Improve the previous code. Fix all bugs. Apply all suggested_fixes. "
            "Address improvements when they improve correctness, reliability, maintainability, or readability."
        )

    try:
        response: Dict[str, Any] = await asyncio.to_thread(
            call_json_model,
            model=CODER_MODEL,
            system_prompt=CODER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    except Exception:
        logger.exception("Coder agent failed")
        raise

    return _normalize_coder_response(response)


def run_coder(
    task: str,
    reviewer_feedback: Optional[Any] = None,
    previous_code: str = "",
    *,
    review_feedback: Optional[Any] = None,
) -> Dict[str, str]:
    return asyncio.run(
        run_coder_async(
            task=task,
            reviewer_feedback=reviewer_feedback,
            previous_code=previous_code,
            review_feedback=review_feedback,
        )
    )
