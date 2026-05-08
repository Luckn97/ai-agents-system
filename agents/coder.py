import json

from utils.llm import call_llm


def run_coder(task: str, review_feedback=None):
    """
    Generates improved Python code based on task + review feedback.
    """

    if review_feedback is None:
        review_feedback = {}

    coder_prompt = f"""
You are a senior Python developer.

TASK:
{task}

REVIEW FEEDBACK:
{json.dumps(review_feedback, indent=2)}

IMPORTANT:
- Return ONLY valid JSON
- No markdown
- No explanations outside JSON
- Escape all newlines correctly

Required JSON format:
{{
    "code": "full code here",
    "rationale": "short explanation"
}}
"""

    response = call_llm(coder_prompt)

    # Falls response schon dict ist
    if isinstance(response, dict):
        return response

    # Falls response string ist
    try:
        return json.loads(response)
    except Exception:
        return {
            "code": "",
            "rationale": "Failed to parse model response"
        }
