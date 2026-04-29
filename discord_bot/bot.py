import sys
from pathlib import Path

import discord
from discord.ext import commands

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def _chunk_text(text: str, chunk_size: int = 1800):
    text = text or ""
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")


@bot.command(name="task")
async def run_task(ctx: commands.Context, *, task_text: str) -> None:
    await ctx.send("Task received. Running workflow...")

    try:
        result = run_workflow(task_text)
    except Exception as exc:
        await ctx.send(f"Workflow failed safely: {str(exc)[:1800]}")
        return

    review = result.get("review", {"bugs": [], "improvements": [], "suggested_fixes": []})
    code = result.get("generated_code", "")
    iterations = result.get("iterations", 0)

    summary = (
        f"✅ Done in {iterations} iteration(s).\n"
        f"Bugs: {review.get('bugs', [])}\n"
        f"Improvements: {review.get('improvements', [])}\n"
        f"Suggested fixes: {review.get('suggested_fixes', [])}"
    )
    await ctx.send(summary[:1900])

    if code:
        for part in _chunk_text(code):
            await ctx.send(f"```python\n{part}\n```")


if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        print("DISCORD_BOT_TOKEN missing. Bot will not start.")
    else:
        bot.run(DISCORD_BOT_TOKEN)
