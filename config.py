import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer.") from exc


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number.") from exc


OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
DISCORD_BOT_TOKEN: Optional[str] = os.getenv("DISCORD_BOT_TOKEN")

CODER_MODEL: str = os.getenv("CODER_MODEL", "gpt-4.1")
REVIEWER_MODEL: str = os.getenv("REVIEWER_MODEL", "gpt-4o-mini")

MAX_ITERATIONS: int = _get_int("MAX_ITERATIONS", 3)
TEMPERATURE: float = _get_float("TEMPERATURE", 0.2)
MAX_TOKENS: int = _get_int("MAX_TOKENS", 2000)
