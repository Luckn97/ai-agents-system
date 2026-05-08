from utils.llm import call_llm


async def run_coder(task: str):
    prompt = f"""
Du bist ein Python Coding Agent.

Aufgabe:
{task}

Gib NUR den Python Code zurück.
"""

    code = await call_llm(prompt)

    return {
        "code": code
    }
