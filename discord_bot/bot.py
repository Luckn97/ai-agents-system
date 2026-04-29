import discord
from discord.ext import commands

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")


@bot.command(name="task")
async def run_task(ctx: commands.Context, *, task_text: str) -> None:
    await ctx.send("Task received. Running multi-agent workflow...")
    result = run_workflow(task_text)

    message = (
        f"✅ Done in {result['iterations']} iteration(s).\n"
        f"Review summary:\n{result['final_review']}"
    )
    await ctx.send(message)


if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        raise ValueError("DISCORD_BOT_TOKEN is not set. Please define it in your environment or .env file.")
    bot.run(DISCORD_BOT_TOKEN)
