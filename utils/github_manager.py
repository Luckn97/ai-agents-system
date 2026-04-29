from pathlib import Path
from typing import Optional

from github import Github
from github.GithubException import GithubException

from config import GITHUB_TOKEN


def push_file_to_github(repo_name: str, file_path: str, commit_message: str) -> str:
    if not GITHUB_TOKEN or not repo_name:
        return "GitHub push skipped (missing GITHUB_TOKEN or GITHUB_REPO)."

    local_path = Path(file_path)
    if not local_path.exists():
        return f"GitHub push skipped ({file_path} not found)."

    content = local_path.read_text(encoding="utf-8")
    gh = Github(GITHUB_TOKEN)

    try:
        repo = gh.get_repo(repo_name)
        try:
            remote_file = repo.get_contents(file_path)
            repo.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=remote_file.sha,
            )
            return f"GitHub updated: {file_path}"
        except GithubException:
            repo.create_file(
                path=file_path,
                message=commit_message,
                content=content,
            )
            return f"GitHub created: {file_path}"
    except GithubException as exc:
        return f"GitHub push failed: {exc.data if hasattr(exc, 'data') else str(exc)}"
