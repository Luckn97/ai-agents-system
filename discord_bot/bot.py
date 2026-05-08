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

        response = (
            "✅ Workflow finished\n\n"
            "## Generated Code\n"
            f"```python\n{code}\n```\n\n"
            "## Review\n"
            f"{review}"
        )

        if len(response) > 1900:
            response = response[:1900]

        await ctx.send(response)

    except Exception as e:
        await ctx.send(f"❌ Workflow failed safely: {str(e)}")


bot.run(TOKEN)
