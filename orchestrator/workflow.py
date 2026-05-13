from agents.coder import run_coder
from agents.reviewer import run_reviewer
from utils.logger import get_logger

logger = get_logger()


async def run_workflow(task: str) -> dict:
    """
    Hauptworkflow:
    1. Code generieren
    2. Review durchführen
    3. Code verbessern
    """

    logger.info("Workflow gestartet")

    # STEP 1: Code generieren
    generated_code = await run_coder(task)

    logger.info("Code erfolgreich generiert")

    # STEP 2: Review + Verbesserung
    review_result = await run_reviewer(
        task=task,
        code=generated_code
    )

    logger.info("Review abgeschlossen")

    return {
        "generated_code": generated_code,
        "review": review_result,
        "final_code": review_result.get(
            "fixed_code",
            generated_code
        )
    }
