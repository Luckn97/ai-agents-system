from utils.llm import call_llm
from utils.logger import get_logger

logger = get_logger()


async def run_reviewer(task: str, code: str) -> dict:
    """
    Reviews generated code and returns:
    - bugs
    - improvements
    - improved code
    """

    prompt = f"""
You are a senior software engineer performing a professional code review.

Your task:
1. Analyze the provided code carefully
2. Find REAL bugs, edge cases, security issues, bad practices
3. Suggest meaningful improvements
4. Improve the code directly
5. Return STRICT JSON only

Be highly critical but practical.
Avoid generic feedback.
Only mention real issues.

TASK:
{task}

CODE:
```python
{code}
