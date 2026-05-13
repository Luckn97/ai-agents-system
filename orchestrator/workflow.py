from agents.coder import run_coder
from agents.coder import improve_code
from agents.reviewer import run_reviewer


async def run_workflow(task: str):
    # STEP 1 - Initial Code
    coder_result = await run_coder(task)

    code = coder_result.get("code", "")

    # STEP 2 - Review
    reviewer_result = await run_reviewer(code)

    review = reviewer_result.get("review", "")
    should_improve = reviewer_result.get("should_improve", False)

    improved = False

    # STEP 3 - Auto Improvement
    if should_improve:
        improved_result = await improve_code(code, review)

        code = improved_result.get("improved_code", code)

        improved = True

    return {
        "code": code,
        "review": review,
        "improved": improved
    }
