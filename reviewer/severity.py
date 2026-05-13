# reviewer/severity.py

SEVERITY_LEVELS = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1
}


def normalize_severity(severity: str) -> str:
    severity = severity.lower().strip()

    if severity not in SEVERITY_LEVELS:
        return "medium"

    return severity


def sort_findings(findings):
    return sorted(
        findings,
        key=lambda f: SEVERITY_LEVELS.get(f.severity, 0),
        reverse=True
    )
