import json
from pathlib import Path
from typing import Any, Dict, List

from config import MEMORY_FILE


def _ensure_memory_file() -> Path:
    path = Path(MEMORY_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")
    return path


def load_history() -> List[Dict[str, Any]]:
    path = _ensure_memory_file()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def append_history(entry: Dict[str, Any]) -> None:
    history = load_history()
    history.append(entry)
    path = _ensure_memory_file()
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
