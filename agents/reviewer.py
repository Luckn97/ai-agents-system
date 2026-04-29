from utils.openai_client import call_openai
import json

REVIEWER_SYSTEM_PROMPT = """
You are a senior code reviewer.

You ONLY respond in valid JSON.

Return this format:

{
  "bugs": [],
  "improvements": [],
  "suggested_fixes": []
}
"""


def run_reviewer(code: str):
    user_prompt = f"""
Review this code:

{code}
"""

    response = call_openai(
        system_prompt=REVIEWER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.2,
        model="gpt-4o-mini"
    )

    try:
        return json.loads(response)
    except Exception:
        return {
            "bugs": [],
            "improvements": ["Reviewer failed to parse response"],
            "suggested_fixes": []
        }
