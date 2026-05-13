# reviewer/resolution.py

def is_finding_resolved(finding, current_code: str) -> bool:
    """
    Prüft ob problematischer Code noch existiert
    """

    snippet = finding.code_snippet.strip()

    if not snippet:
        return False

    return snippet not in current_code
