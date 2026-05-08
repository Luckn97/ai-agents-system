from agents.coder import run_coder
from agents.reviewer import run_reviewer


async def run_workflow(task: str):
    coder_result = await run_coder(task)

    code = coder_result.get("code", "")

    reviewer_result = await run_reviewer(code)

    review = reviewer_result.get("review", "")

    return {
        "code": code,
        "review": review
    }
