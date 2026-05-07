from config import MAX_TOKENS, TEMPERATURE
from utils.llm import get_openai_client


def call_openai(
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = TEMPERATURE,
) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""
