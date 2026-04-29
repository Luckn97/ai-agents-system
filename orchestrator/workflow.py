from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from agents.coder import run_coder
from agents.reviewer import run_reviewer
from config import GENERATED_FILE, MAX_ITERATIONS
from utils.github_manager import push_file_to_github
from utils.logger import log_event
from utils.memory_manager import append_history


def _save_generated_code(code: str) -> None:
    target = Path(GENERATED_FILE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(code, encoding="utf-8")


def run_workflow(task: str) -> Dict[str, Any]:
    task = task or ""
    iteration = 0
    code = ""
    review: Dict[str, List[str]] = {"bugs": [], "improvements": [], "suggested_fixes": []}

    log_event("workflow_started", {"task": task})

    feedback = ""
    for idx in range(1, MAX_ITERATIONS + 1):
        iteration = idx
        code = run_coder(task, review_feedback=feedback)
        _save_generated_code(code)
        log_event("coder_output", {"iteration": idx, "code_length": len(code)})

        review = run_reviewer(code)
        log_event("reviewer_output", {"iteration": idx, "review": review})

        if not review.get("bugs"):
            break

        feedback = (
            f"Bugs: {review.get('bugs', [])}\n"
            f"Improvements: {review.get('improvements', [])}\n"
            f"Suggested fixes: {review.get('suggested_fixes', [])}"
        )

    repo_name = __import__("os").getenv("GITHUB_REPO", "")
    github_status = push_file_to_github(
        repo_name=repo_name,
        file_path=GENERATED_FILE,
        commit_message=f"Update generated code ({datetime.now(timezone.utc).isoformat()})",
    )
    log_event("github_push", {"status": github_status})

    memory_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "iterations": iteration,
        "generated_code": code,
        "review": review,
        "github_status": github_status,
    }
    append_history(memory_entry)
    log_event("memory_saved", {"iterations": iteration})

    result = {
        "iterations": iteration,
        "generated_code": code,
        "review": review,
    }
    log_event("workflow_finished", result)
    return result
