import sys
from pathlib import Path

import discord
from discord.ext import commands

# Projektroot importierbar machen
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.command(name="task")
async def run_task(ctx, *, task_text: str):
    await ctx.send("⚙️ Task received. Running multi-agent workflow...")

    try:
        result = run_workflow(task_text)

        generated_code = result.get("generated_code", "No code generated.")
        review = result.get("review", "No review available.")

        message = (
            f"✅ Done in {result.get('iterations', 1)} iteration(s).\n\n"
            f"## GENERATED CODE:\n"
            f"```python\n{generated_code}\n```\n\n"
            f"## REVIEW:\n"
            f"{review}"
        )

        # Discord Nachrichtenlimit
        if len(message) > 1900:
            message = message[:1900] + "\n\n...output truncated"

        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"❌ Error:\n```{str(e)}```")


bot.run(DISCORD_BOT_TOKEN)
