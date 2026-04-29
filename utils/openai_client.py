from openai import OpenAI

from config import OPENAI_API_KEY

_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def call_openai(model: str, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    if _client is None:
        return ""

    response = _client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""
