import asyncio
from agents.coder import run_coder
from agents.reviewer import run_reviewer

from config import MAX_ITERATIONS
from utils.logger import logger
from utils.file_manager import write_file


def run_workflow(task: str):
    logger.info(f"Starting workflow for task: {task}")

    final_files = []
    rationale = ""
    review = {}

    feedback = ""

    for iteration in range(MAX_ITERATIONS):
        logger.info(f"Iteration {iteration + 1}")

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
