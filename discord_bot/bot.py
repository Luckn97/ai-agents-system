import discord
from discord.ext import commands

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow
from utils.logger import get_logger

logger = get_logger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Bot logged in as {bot.user}")
    print(f"✅ Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")


@bot.command()
async def task(ctx, *, prompt: str):
    await ctx.send("⚙️ Running autonomous workflow...")

    try:
        result = await run_workflow(prompt)

        code = result.get("code", "No code generated.")
        review = result.get("review", "No review.")

        response = f"""
✅ Done.

## GENERATED CODE
```python
{code}
