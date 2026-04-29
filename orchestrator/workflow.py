import json

from agents.coder import run_coder
from agents.reviewer import run_reviewer

MAX_ITERATIONS = 3


def run_workflow(task: str):
    review_feedback = ""

    final_code = {}
    final_review = {}

    for iteration in range(MAX_ITERATIONS):

        coder_response = run_coder(
            task=task,
            review_feedback=review_feedback
        )

        try:
            parsed_code = json.loads(coder_response)
        except Exception:
            parsed_code = {
                "code": str(coder_response),
                "rationale": "Failed to parse structured response."
            }

        code_only = parsed_code.get("code", "")

        review = run_reviewer(code_only)

        final_code = parsed_code
        final_review = review

        bugs = review.get("bugs", [])

        if not bugs:
            break

        review_feedback = json.dumps(review)

    return {
        "code": final_code,
        "review": final_review,
        "iterations": iteration + 1
    }
