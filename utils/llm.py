import json
from typing import Any, Dict, Optional

from openai import OpenAI

from config import MAX_TOKENS, OPENAI_API_KEY, TEMPERATURE
from utils.logger import get_logger

logger = get_logger(__name__)
_client: Optional[OpenAI] = None


def get_openai_client() -> OpenAI:
    global _client

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)

    return _client


def parse_json_object(content: str) -> Dict[str, Any]:
    text = (content or "").strip()
    if not text:
        raise ValueError("LLM response was empty.")

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        parsed = json.loads(text[start : end + 1])

    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object.")

    return parsed


def call_json_model(
    *,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS,
) -> Dict[str, Any]:
    logger.info("Calling OpenAI model %s", model)
    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content or ""
    return parse_json_object(content)
