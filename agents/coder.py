from utils.openai_client import call_openai

CODER_SYSTEM_PROMPT = """
You are a senior Python software engineer.

You ONLY respond in valid JSON.

Return this exact JSON format:

{
  "code": "python code here",
  "rationale": "short explanation"
}

Rules:
- Generate clean code
- Do not include markdown
- Do not use triple backticks
- Always include code
"""


def run_coder(task: str):
    user_prompt = f"""
Task:
{task}

Generate Python code.
"""

    response = call_openai(
        system_prompt=CODER_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=0.3,
        model="gpt-4.1-mini"
    )

    return response
