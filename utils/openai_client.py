from openai import OpenAI

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def call_openai(model: str, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Central OpenAI call function used by all agents.

    Args:
        model: Model name provided by agent-level configuration.
        system_prompt: System instruction for the model.
        user_prompt: User task payload.
        temperature: Sampling temperature.
    """
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""
