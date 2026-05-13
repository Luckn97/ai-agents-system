# reviewer/deduplication.py

from difflib import SequenceMatcher


SIMILARITY_THRESHOLD = 0.88


def calculate_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def is_duplicate(new_finding, existing_findings):
    for existing in existing_findings:

        if existing.id == new_finding.id:
            return True

        title_similarity = calculate_similarity(
            new_finding.title,
            existing.title
        )

        if (
            title_similarity >= SIMILARITY_THRESHOLD
            and new_finding.file_path == existing.file_path
        ):
            return True

    return False
