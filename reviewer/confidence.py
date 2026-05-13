# reviewer/confidence.py

def calculate_confidence(issue_type: str) -> float:

    confidence_map = {
        "security": 0.95,
        "bug": 0.90,
        "performance": 0.82,
        "maintainability": 0.70,
        "style": 0.45
    }

    return confidence_map.get(issue_type, 0.60)
