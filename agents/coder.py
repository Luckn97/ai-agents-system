import json

from config import CODER_MODEL, MAX_TOKENS, TEMPERATURE
from utils.llm import client
from utils.logger import logger


def run_coder(task: str, review_feedback: str = ""):
    logger.info("Running coder agent...")

    prompt = f"""
You are an expert Python software engineer.

TASK:
{task}

REVIEW FEEDBACK:
{review_feedback}

You MUST respond ONLY with valid JSON.

FORMAT:

{{
    "files": [
        {{
            "path": "relative/file/path.py",
            "content": "FULL FILE CONTENT"
        }}
    ],
    "rationale": "SHORT EXPLANATION"
}}

RULES:
- Always create complete files
- Always include file paths
- Never use markdown
- Never use triple backticks
- Content must be raw file content only
"""

    response = client.chat.completions.create(
        model=CODER_MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {
                "role": "system",
                "content": "You are a senior AI coding agent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    logger.info("Coder response received.")

    try:
        parsed = json.loads(content)

        return {
            "files": parsed.get("files", []),
            "rationale": parsed.get("rationale", "")
        }

    except Exception as e:
        logger.error(f"Failed to parse coder JSON: {e}")

        return {
            "files": [],
            "rationale": "JSON parsing failed."
        }
