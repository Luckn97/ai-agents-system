import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Agent-specific models (Railway variable compatible)
CODER_MODEL = os.getenv("CODER_MODEL", "gpt-4.1")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "gpt-4o-mini")

# Auto-fix upper bound
MAX_ITERATIONS = 3

# Repo/file settings for generated output
GENERATED_DIR = "generated"
GENERATED_FILE = "generated/generated_code.py"
MEMORY_FILE = "memory/history.json"
