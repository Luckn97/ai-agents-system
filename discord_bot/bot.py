import os
import discord
from discord.ext import commands
from orchestrator.workflow import run_workflow

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def task(ctx, *, task_text: str):
    try:
        await ctx.send("⚙️ Running autonomous workflow...")

        result = await run_workflow(task_text)

        code = result.get("code", "No code generated")
        review = result.get("review", "No review generated")

        response = f"""
✅ Workflow finished

## Generated Code
```python
{code}
