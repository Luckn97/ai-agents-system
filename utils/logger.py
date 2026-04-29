import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

LOG_FILE = Path("run_logs.jsonl")


def log_event(event_type: str, data: Dict[str, Any]) -> None:
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "data": data,
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def read_logs() -> List[Dict[str, Any]]:
    if not LOG_FILE.exists():
        return []

    lines: List[Dict[str, Any]] = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                lines.append(json.loads(line))
            except json.JSONDecodeError:
                lines.append({"event_type": "malformed", "data": {"line": line}})
    return lines
