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


def _strip_json_fence(content: str) -> str:
    text = (content or "").strip()
    if not text.startswith("```"):
        return text

    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def parse_json_object(content: str) -> Dict[str, Any]:
    text = _strip_json_fence(content)
    if not text:
        raise ValueError("LLM response was empty.")

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        parsed = None
        for index, character in enumerate(text):
            if character != "{":
                continue
            try:
                candidate, _ = decoder.raw_decode(text[index:])
            except json.JSONDecodeError:
                continue
            if isinstance(candidate, dict):
                parsed = candidate
                break
        if parsed is None:
            raise

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
    parse_retries: int = 2,
) -> Dict[str, Any]:
    client = get_openai_client()
    last_error: Optional[Exception] = None
    effective_prompt = user_prompt

    for attempt in range(1, parse_retries + 2):
        logger.info("Calling OpenAI model %s (attempt %s)", model, attempt)
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": effective_prompt},
            ],
        )

        content = response.choices[0].message.content or ""
        try:
            return parse_json_object(content)
        except (json.JSONDecodeError, ValueError) as exc:
            last_error = exc
            logger.warning("Failed to parse JSON response from %s: %s", model, exc)
            effective_prompt = (
                f"{user_prompt}\n\n"
                "Your previous response was not a valid JSON object. "
                "Retry now with valid JSON only and no markdown."
            )

    raise ValueError(f"Failed to parse JSON response from {model}.") from last_error
