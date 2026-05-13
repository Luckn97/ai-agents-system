import os

import discord
from discord.ext import commands

from orchestrator.workflow import run_workflow

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Bot eingeloggt als: {bot.user}")


@bot.command()
async def task(ctx, *, prompt: str):
    """
    Führt den autonomen Workflow aus
    """

    try:
        await ctx.send("⚙️ Starte autonomen Workflow...")

        result = await run_workflow(prompt)

        generated_code = result.get(
            "generated_code",
            ""
        )

        review = result.get(
            "review",
            {}
        )

        final_code = result.get(
            "final_code",
            ""
        )

        bugs = review.get(
            "bugs",
            []
        )

        improvements = review.get(
            "improvements",
            []
        )

        bugs_text = "\n".join(
            f"- {bug}" for bug in bugs
        )

        improvements_text = "\n".join(
            f"- {item}" for item in improvements
        )

        if not bugs_text:
            bugs_text = "- Keine Bugs gefunden"

        if not improvements_text:
            improvements_text = "- Keine Verbesserungen gefunden"

        response = f"""
# ✅ Workflow abgeschlossen

## Generierter Code

```python
{generated_code[:1200]}
