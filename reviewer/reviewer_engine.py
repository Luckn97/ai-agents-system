# reviewer/reviewer_engine.py

from reviewer.models import Finding
from reviewer.severity import normalize_severity, sort_findings
from reviewer.deduplication import is_duplicate
from reviewer.confidence import calculate_confidence


class ReviewerEngine:

    def __init__(self):
        self.findings = []

    def add_finding(
        self,
        title,
        description,
        severity,
        file_path,
        line,
        code_snippet,
        category
    ):

        severity = normalize_severity(severity)

        confidence = calculate_confidence(category)

        finding = Finding(
            title=title,
            description=description,
            severity=severity,
            confidence=confidence,
            file_path=file_path,
            line=line,
            code_snippet=code_snippet,
            category=category
        )

        finding.id = finding.generate_id()

        if is_duplicate(finding, self.findings):
            print(f"[SKIPPED DUPLICATE] {finding.title}")
            return

        self.findings.append(finding)

    def get_findings(self):
        return [
            f.to_dict()
            for f in sort_findings(self.findings)
        ]
