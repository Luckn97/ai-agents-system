from config import CODER_MODEL
from utils.openai_client import call_openai

coder_prompt = (
    "You are a senior Python software engineer. "
    "Return ONLY raw Python code. "
    "No markdown fences. No explanation. No rationale."
# Dedicated prompt for the Coder agent.
coder_prompt = (
    "You are a senior Python software engineer. "
    "Generate clean, executable code and short explanations."
)


def run_coder(task: str, review_feedback: str = "") -> str:
    feedback = f"\n\nReview feedback:\n{review_feedback}" if review_feedback else ""
    user_prompt = f"Task:\n{task}{feedback}\n\nReturn only executable Python code."
    return call_openai(CODER_MODEL, coder_prompt, user_prompt, temperature=0.2)
