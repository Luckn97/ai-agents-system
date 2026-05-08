import asyncio

from agents.coder import run_coder
from agents.reviewer import run_reviewer
from utils.logger import get_logger

logger = get_logger(__name__)


async def run_workflow(task: str):
    logger.info(f"Starting workflow for task: {task}")

    code = await asyncio.to_thread(run_coder, task)

    review = await asyncio.to_thread(run_reviewer, code)

    return {
        "code": code,
        "review": review
    }
