import asyncio
import json
from typing import Any, Dict, List, Optional, TypedDict

from agents.coder import run_coder_async
from agents.reviewer import ReviewResult, run_reviewer_async
from config import MAX_ITERATIONS
from utils.logger import get_logger, log_event

logger = get_logger(__name__)


class WorkflowState(TypedDict):
    previous_code: str
    reviewer_history: List[ReviewResult]
    improvements_applied: bool


class WorkflowResult(TypedDict):
    code: Dict[str, str]
    review: ReviewResult
    iterations: int
    state: WorkflowState


def _has_feedback(review: ReviewResult) -> bool:
    return bool(
        review.get("bugs")
        or review.get("improvements")
        or review.get("suggested_fixes")
    )


def _build_reviewer_feedback(review: ReviewResult) -> str:
    return json.dumps(review, ensure_ascii=False)


async def run_workflow_async(task: str) -> WorkflowResult:
    logger.info("Starting workflow")
    log_event("workflow_started", {"task": task})

    previous_code = ""
    reviewer_feedback: Optional[str] = None
    reviewer_history: List[ReviewResult] = []
    improvements_applied = False
    final_code: Dict[str, str] = {"code": "", "rationale": ""}
    final_review: ReviewResult = {
        "bugs": [],
        "improvements": [],
        "suggested_fixes": [],
    }
    iterations_completed = 0

    try:
        for iteration in range(1, MAX_ITERATIONS + 1):
            iterations_completed = iteration
            logger.info("Workflow iteration %s of %s", iteration, MAX_ITERATIONS)
            log_event(
                "workflow_iteration_started",
                {
                    "iteration": iteration,
                    "has_previous_code": bool(previous_code),
                    "has_reviewer_feedback": bool(reviewer_feedback),
                },
            )

            final_code = await run_coder_async(
                task=task,
                reviewer_feedback=reviewer_feedback,
                previous_code=previous_code,
            )

            if reviewer_feedback:
                improvements_applied = True

            current_code = final_code.get("code", "")
            final_review = await run_reviewer_async(current_code)
            reviewer_history.append(final_review)

            has_feedback = _has_feedback(final_review)
            log_event(
                "workflow_iteration_completed",
                {
                    "iteration": iteration,
                    "bugs": len(final_review.get("bugs", [])),
                    "improvements": len(final_review.get("improvements", [])),
                    "suggested_fixes": len(final_review.get("suggested_fixes", [])),
                    "will_retry": has_feedback and iteration < MAX_ITERATIONS,
                },
            )

            if not has_feedback:
                logger.info("Workflow stopping: reviewer returned no bugs or improvements")
                break

            if iteration >= MAX_ITERATIONS:
                logger.info("Workflow stopping: max iterations reached")
                break

            previous_code = current_code
            reviewer_feedback = _build_reviewer_feedback(final_review)

    except Exception:
        logger.exception("Workflow failed")
        log_event(
            "workflow_failed",
            {
                "iterations": iterations_completed,
                "reviews": len(reviewer_history),
            },
        )
        raise

    result: WorkflowResult = {
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


def run_workflow(task: str) -> WorkflowResult:
    return asyncio.run(run_workflow_async(task))
