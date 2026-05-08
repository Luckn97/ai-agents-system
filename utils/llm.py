import os
import json
from openai import OpenAI

# OpenAI Client initialisieren
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def call_llm(prompt: str):
    """
    Sends prompt to OpenAI and returns parsed JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional coding AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)

    except Exception:
        return {
            "raw_response": content
        }


def call_json_model(prompt: str):
    """
    Backwards compatibility wrapper.
    Alte Agents können weiterhin call_json_model benutzen.
    """

    return call_llm(prompt)
