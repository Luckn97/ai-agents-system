import json
from typing import Any, Dict, List

from agents.coder import run_coder
from agents.reviewer import run_reviewer
from config import MAX_ITERATIONS
from utils.logger import get_logger, log_event

logger = get_logger(__name__)


def _build_review_feedback(review: Dict[str, List[str]]) -> str:
    return json.dumps(review, ensure_ascii=False)


def run_workflow(task: str) -> Dict[str, Any]:
    logger.info("Starting workflow")
    log_event("workflow_started", {"task": task})

    review_feedback = ""
    final_code: Dict[str, str] = {"code": "", "rationale": ""}
    final_review: Dict[str, List[str]] = {
        "bugs": [],
        "improvements": [],
        "suggested_fixes": [],
    }
    iterations_completed = 0

    for iteration in range(1, MAX_ITERATIONS + 1):
        iterations_completed = iteration
        logger.info("Workflow iteration %s of %s", iteration, MAX_ITERATIONS)
        log_event("workflow_iteration_started", {"iteration": iteration})

        final_code = run_coder(task=task, review_feedback=review_feedback)
        final_review = run_reviewer(final_code.get("code", ""))

        log_event(
            "workflow_iteration_completed",
            {
                "iteration": iteration,
                "bugs": len(final_review.get("bugs", [])),
                "improvements": len(final_review.get("improvements", [])),
                "suggested_fixes": len(final_review.get("suggested_fixes", [])),
            },
        )

        if not final_review.get("bugs"):
            logger.info("Workflow completed without blocking bugs")
            break

        review_feedback = _build_review_feedback(final_review)

    result: Dict[str, Any] = {
        "code": final_code,
        "review": final_review,
        "iterations": iterations_completed,
    }

    log_event("workflow_completed", {"iterations": iterations_completed})
    return result
