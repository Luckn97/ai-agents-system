from utils.llm import call_llm


async def run_reviewer(code: str):
    prompt = f"""
Du bist ein Senior Code Reviewer.

Analysiere folgenden Python Code:

{code}

Antworte im Format:

BUGS:
- ...

IMPROVEMENTS:
- ...
"""

    review = await call_llm(prompt)

    return {
        "review": review
    }
