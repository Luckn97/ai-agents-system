import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

# Agent-specific model configuration (overridable via environment variables / Railway Variables)
CODER_MODEL = os.getenv("CODER_MODEL", "gpt-4.1")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "gpt-4o-mini")

MAX_ITERATIONS = 2

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please define it in your environment or .env file.")
