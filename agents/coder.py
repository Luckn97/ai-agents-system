from utils.llm import call_llm


async def run_coder(task: str):
    prompt = f"""
Du bist ein Python Coding Agent.

Aufgabe:
{task}

WICHTIG:
- Antworte NUR mit Python Code
- Keine Erklärungen
- Kein Markdown
"""

    code = await call_llm(prompt)

    return {
        "code": code
    }


async def improve_code(original_code: str, review: str):
    prompt = f"""
Du bist ein Senior Python Engineer.

Hier ist der ursprüngliche Code:

{original_code}

Hier ist das Reviewer Feedback:

{review}

Verbessere den Code basierend auf dem Feedback.

WICHTIG:
- Gib NUR den verbesserten Python Code zurück
- Keine Erklärungen
- Kein Markdown
"""

    improved_code = await call_llm(prompt)

    return {
        "improved_code": improved_code
    }
