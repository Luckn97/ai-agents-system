from utils.llm import call_llm
from utils.logger import get_logger

logger = get_logger()


async def run_reviewer(task: str, code: str) -> dict:
    """
    Führt einen intelligenten Code-Review durch
    und gibt Bugs, Verbesserungen und verbesserten Code zurück.
    """

    prompt = f"""
Du bist ein Senior Software Engineer und führst ein professionelles Code Review durch.

AUFGABEN:
1. Analysiere den Code sorgfältig
2. Finde echte Bugs, Edge Cases und schlechte Praktiken
3. Finde mögliche Sicherheitsprobleme
4. Schlage sinnvolle Verbesserungen vor
5. Verbessere den Code direkt
6. Antworte AUSSCHLIESSLICH als JSON

WICHTIG:
- Keine generischen Aussagen
- Nur echte Probleme nennen
- Keine Erklärungen außerhalb des JSONs
- Der verbesserte Code muss vollständig sein

TASK:
{task}

CODE:
```python
{code}
