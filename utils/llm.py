import os
import json
from openai import OpenAI

# OpenAI Client initialisieren
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def call_llm(prompt: str):
    """
    Sends a prompt to OpenAI and returns parsed JSON.
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

    # JSON sicher parsen
    try:
        return json.loads(content)
    except Exception:
        return {
            "raw_response": content
        }
