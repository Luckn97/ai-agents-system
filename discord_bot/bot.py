import sys
from pathlib import Path

import discord
from discord.ext import commands

# Projektpfad fix für Railway
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
    print(f"Logged in as {bot.user}")


@bot.command(name="task")
async def run_task(ctx, *, task_text: str):

    await ctx.send("Task received. Running multi-agent workflow...")

    result = run_workflow(task_text)

    generated_code = result.get("code", "No code generated.")

    message = (
        f"✅ Done in {result['iterations']} iteration(s).\n\n"
        f"## GENERATED CODE\n"
        f"```python\n{generated_code[:3500]}\n```\n\n"
        f"## REVIEW SUMMARY\n"
        f"{result['review']}"
    )

    await ctx.send(message)


bot.run(DISCORD_BOT_TOKEN)
