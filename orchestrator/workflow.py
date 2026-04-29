from agents.coder import run_coder
from agents.reviewer import run_reviewer

MAX_ITERATIONS = 2


def run_workflow(task: str):

    current_code = ""
    review_result = {}

    for iteration in range(MAX_ITERATIONS):

        current_code = run_coder(task, current_code)

        review_result = run_reviewer(current_code)

        bugs = review_result.get("bugs", [])
        improvements = review_result.get("improvements", [])
        suggested_fixes = review_result.get("suggested_fixes", [])

        if not bugs and not improvements:
            break

        feedback = f"""
        Bugs:
        {bugs}

        Improvements:
        {improvements}

        Suggested fixes:
        {suggested_fixes}
        """

        task = f"""
        Original task:
        {task}

        Reviewer feedback:
        {feedback}
        """

    return {
        "iterations": iteration + 1,
        "review": review_result,
        "code": current_code
    }
