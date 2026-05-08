from agents.coder import run_coder
<<<<<<< codex/refactor-ai-multi-agent-discord-system-lub81l
from agents.reviewer import ReviewResult, run_reviewer
=======
from agents.reviewer import run_reviewer

>>>>>>> main
from config import MAX_ITERATIONS
from utils.logger import logger
from utils.file_manager import write_file


def run_workflow(task: str):
    logger.info(f"Starting workflow for task: {task}")

<<<<<<< codex/refactor-ai-multi-agent-discord-system-lub81l
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
=======
    final_files = []
    rationale = ""
    review = {}
>>>>>>> main

    feedback = ""

    for iteration in range(MAX_ITERATIONS):
        logger.info(f"Iteration {iteration + 1}")

<<<<<<< codex/refactor-ai-multi-agent-discord-system-lub81l
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
=======
        coder_result = run_coder(
            task=task,
            review_feedback=feedback
        )

        generated_files = coder_result.get("files", [])
        rationale = coder_result.get("rationale", "")

        final_files = generated_files

        combined_code = ""

        for file in generated_files:
            path = file.get("path", "")
            content = file.get("content", "")

            combined_code += f"\nFILE: {path}\n{content}\n"

            write_file(path, content)

        review = run_reviewer(combined_code)

        bugs = review.get("bugs", [])

        high_severity_bugs = [
            bug for bug in bugs
            if isinstance(bug, dict)
            and bug.get("severity") == "high"
        ]

        if not high_severity_bugs:
            logger.info("No high severity bugs found.")

            break

        feedback = f"""
Reviewer found issues:

{review}
"""

    logger.info("Workflow completed.")

    return {
        "iterations": iteration + 1,
        "files": final_files,
        "rationale": rationale,
        "review": review,
        "improvements_applied": iteration > 0
    }
>>>>>>> main
