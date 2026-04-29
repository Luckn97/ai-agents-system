from agents.coder import run_coder
from agents.reviewer import run_reviewer


def run_workflow(task: str):
    """
    Einfacher Multi-Agent Workflow
    """

    generated_code = run_coder(task)

    review_result = run_reviewer(generated_code)

    return {
        "iterations": 1,
        "generated_code": generated_code,
        "review": review_result,
    }
