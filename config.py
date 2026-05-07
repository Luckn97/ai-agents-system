import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# API KEYS
# =========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is not set. Please define it in your environment or .env file."
    )

if not DISCORD_BOT_TOKEN:
    raise ValueError(
        "DISCORD_BOT_TOKEN is not set. Please define it in your environment or .env file."
    )

# =========================
# MODEL CONFIG
# =========================

CODER_MODEL = "gpt-5.5"
REVIEWER_MODEL = "gpt-4o-mini"

# =========================
# WORKFLOW SETTINGS
# =========================

MAX_ITERATIONS = 2
TEMPERATURE = 0.2
MAX_TOKENS = 2000
