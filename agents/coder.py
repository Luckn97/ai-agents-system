from typing import Any, Dict

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
  "rationale": "string containing a concise explanation"
}

Rules:
- Return valid JSON only.
- Do not use markdown.
- Do not use triple backticks.
- Always include complete code in the code field.
- Keep the implementation minimal, clean, and production-ready.
""".strip()


def run_coder(task: str, review_feedback: str = "") -> Dict[str, str]:
    logger.info("Running coder agent")

    user_prompt = f"Task:\n{task.strip()}"

    if review_feedback:
        user_prompt += (
            "\n\nPrevious review feedback:\n"
            f"{review_feedback}\n\n"
            "Improve the code using this feedback."
        )

    response: Dict[str, Any] = call_json_model(
        model=CODER_MODEL,
        system_prompt=CODER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    return {
        "code": str(response.get("code", "")).strip(),
        "rationale": str(response.get("rationale", "")).strip(),
    }
