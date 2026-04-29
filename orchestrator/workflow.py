from typing import Dict, List

from agents.coder import run_coder
from agents.reviewer import run_reviewer
from config import MAX_ITERATIONS
from utils.logger import log_event


def _has_issues(review: Dict[str, List[str]]) -> bool:
    return bool(review["bugs"] or review["improvements"] or review["suggested_fixes"])


def run_workflow(task: str) -> Dict[str, object]:
    log_event("workflow_started", {"task": task})

    latest_code = run_coder(task)
    log_event("coder_output", {"iteration": 1, "output": latest_code})

    latest_review = run_reviewer(latest_code)
    log_event("reviewer_output", {"iteration": 1, "review": latest_review})

    iteration = 1
    while iteration < MAX_ITERATIONS and _has_issues(latest_review):
        iteration += 1
        feedback = (
            f"Bugs: {latest_review['bugs']}\n"
            f"Improvements: {latest_review['improvements']}\n"
            f"Suggested fixes: {latest_review['suggested_fixes']}"
        )
        latest_code = run_coder(task, review_feedback=feedback)
        log_event("coder_output", {"iteration": iteration, "output": latest_code})

        latest_review = run_reviewer(latest_code)
        log_event("reviewer_output", {"iteration": iteration, "review": latest_review})

    result = {
        "task": task,
        "iterations": iteration,
        "final_code": latest_code,
        "final_review": latest_review,
    }
    log_event("workflow_finished", result)
    return result
