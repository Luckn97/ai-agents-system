from config import CODER_MODEL
from utils.openai_client import call_openai

# Dedicated prompt for the Coder agent.
coder_prompt = (
    "You are a senior Python software engineer. "
    "Generate clean, executable code and short explanations."
)


def run_coder(task: str, review_feedback: str = "") -> str:
    feedback_block = f"\n\nReview feedback to apply:\n{review_feedback}" if review_feedback else ""
    user_prompt = (
        "Task:\n"
        f"{task}\n"
        "Return only the improved code solution and a concise rationale."
        f"{feedback_block}"
    )

    # Model is loaded from environment-backed config for Railway compatibility.
    return call_openai(CODER_MODEL, coder_prompt, user_prompt, temperature=0.3)
