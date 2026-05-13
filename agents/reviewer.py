from utils.llm import call_llm


async def run_reviewer(code: str):
    prompt = f"""
Du bist ein Senior Code Reviewer.

Analysiere folgenden Python Code:

{code}

Suche nach:
- Bugs
- Verbesserungen
- Clean Code Problemen
- Fehlender Error Handling
- Performance Problemen

Antworte EXAKT im Format:

BUGS:
- ...

IMPROVEMENTS:
- ...

SHOULD_IMPROVE:
YES oder NO
"""

    review = await call_llm(prompt)

    should_improve = "YES" in review.upper()

    return {
        "review": review,
        "should_improve": should_improve
    }
