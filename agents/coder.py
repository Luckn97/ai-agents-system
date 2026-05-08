import json

from config import CODER_MODEL, MAX_TOKENS, TEMPERATURE
from utils.llm import client
from utils.logger import logger


def run_coder(task: str, review_feedback: str = ""):
    logger.info("Running coder agent...")

<<<<<<< codex/refactor-ai-multi-agent-discord-system-lub81l
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
- Always include complete code in the code field.
- Keep the implementation minimal, clean, and production-ready.
- You MUST fix all reviewer issues when reviewer feedback is provided.
- Preserve existing behavior unless a reviewer issue requires a change.
""".strip()
=======
    prompt = f"""
You are an expert Python software engineer.

TASK:
{task}
>>>>>>> main

REVIEW FEEDBACK:
{review_feedback}

<<<<<<< codex/refactor-ai-multi-agent-discord-system-lub81l
def run_coder(
    task: str,
    review_feedback: str = "",
    previous_code: str = "",
) -> Dict[str, str]:
    logger.info("Running coder agent")
=======
You MUST respond ONLY with valid JSON.
>>>>>>> main

FORMAT:

<<<<<<< codex/refactor-ai-multi-agent-discord-system-lub81l
    if previous_code:
        user_prompt += f"\n\nPrevious code to improve:\n{previous_code.strip()}"

    if review_feedback:
        user_prompt += (
            "\n\nReviewer feedback to apply:\n"
            f"{review_feedback}\n\n"
            "You MUST fix all reviewer issues. Apply every suggested fix that improves correctness, safety, or maintainability."
        )
=======
{{
    "files": [
        {{
            "path": "relative/file/path.py",
            "content": "FULL FILE CONTENT"
        }}
    ],
    "rationale": "SHORT EXPLANATION"
}}
>>>>>>> main

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
