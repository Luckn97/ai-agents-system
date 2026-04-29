from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

LOG_FILE = Path("run_logs.jsonl")


def log_event(event_type: str, data: Dict[str, object]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = {"timestamp": timestamp, "event_type": event_type, "data": data}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{payload}\n")


def read_logs() -> List[str]:
    if not LOG_FILE.exists():
        return []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]
