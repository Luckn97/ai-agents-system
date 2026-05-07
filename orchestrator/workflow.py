import json
from typing import Any, Dict, List

from agents.coder import run_coder
from agents.reviewer import ReviewResult, run_reviewer
from config import MAX_ITERATIONS
from utils.logger import get_logger, log_event

logger = get_logger(__name__)


def _has_high_severity_bugs(review: ReviewResult) -> bool:
    return any(bug.get("severity") == "high" for bug in review.get("bugs", []))


def _has_feedback(review: ReviewResult) -> bool:
    return bool(
        review.get("bugs")
        or review.get("improvements")
        or review.get("suggested_fixes")
    )


def _build_review_feedback(review: ReviewResult) -> str:
    return json.dumps(review, ensure_ascii=False)


def run_workflow(task: str) -> Dict[str, Any]:
    logger.info("Starting workflow")
    log_event("workflow_started", {"task": task})

    previous_code = ""
    review_feedback = ""
    reviewer_history: List[ReviewResult] = []
    improvements_applied = False
    final_code: Dict[str, str] = {"code": "", "rationale": ""}
    final_review: ReviewResult = {
        "bugs": [],
        "improvements": [],
        "suggested_fixes": [],
    }
    iterations_completed = 0

    for iteration in range(1, MAX_ITERATIONS + 1):
        iterations_completed = iteration
        logger.info("Workflow iteration %s of %s", iteration, MAX_ITERATIONS)
        log_event(
            "workflow_iteration_started",
            {
                "iteration": iteration,
                "has_previous_code": bool(previous_code),
                "has_review_feedback": bool(review_feedback),
            },
        )

        final_code = run_coder(
            task=task,
            review_feedback=review_feedback,
            previous_code=previous_code,
        )
        current_code = final_code.get("code", "")
        final_review = run_reviewer(current_code)
        reviewer_history.append(final_review)

        high_bug_count = sum(
            1 for bug in final_review.get("bugs", []) if bug.get("severity") == "high"
        )

        log_event(
            "workflow_iteration_completed",
            {
                "iteration": iteration,
                "bugs": len(final_review.get("bugs", [])),
                "high_severity_bugs": high_bug_count,
                "improvements": len(final_review.get("improvements", [])),
                "suggested_fixes": len(final_review.get("suggested_fixes", [])),
            },
        )

        if not _has_high_severity_bugs(final_review):
            logger.info("Workflow stopping: no high severity bugs remain")
            break

        if iteration >= MAX_ITERATIONS:
            logger.info("Workflow stopping: max iterations reached")
            break

        previous_code = current_code
        review_feedback = _build_review_feedback(final_review)
        improvements_applied = _has_feedback(final_review)

    result: Dict[str, Any] = {
        "code": final_code,
        "review": final_review,
        "iterations": iterations_completed,
        "state": {
            "previous_code": previous_code,
            "reviewer_history": reviewer_history,
            "improvements_applied": improvements_applied,
        },
    }

    log_event(
        "workflow_completed",
        {
            "iterations": iterations_completed,
            "improvements_applied": improvements_applied,
            "reviews": len(reviewer_history),
        },
    )
    return result
