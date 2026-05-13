
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import hashlib


@dataclass
class Finding:
    title: str
    description: str
    severity: str
    file_path: str
    line: int
    code_snippet: str
    category: str
    confidence: float = 0.8

    id: Optional[str] = None
    status: str = "open"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def generate_id(self) -> str:
        raw = f"{self.title}:{self.file_path}:{self.line}:{self.category}"

        hashed = hashlib.sha256(raw.encode()).hexdigest()[:10]

        prefix = self.category.upper()

        return f"{prefix}-{hashed}"

    def to_dict(self):
        if not self.id:
            self.id = self.generate_id()

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "confidence": self.confidence,
            "file_path": self.file_path,
            "line": self.line,
            "code_snippet": self.code_snippet,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at
        }
