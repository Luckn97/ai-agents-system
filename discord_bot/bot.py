import discord
from discord.ext import commands

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="task")
async def run_task(ctx, *, task_text: str):
    await ctx.send("⚙️ Running autonomous workflow...")

    try:
        result = run_workflow(task_text)

        files = result.get("files", [])
        rationale = result.get("rationale", "")
        review = result.get("review", {})

        message = f"""
✅ Workflow Complete

Iterations:
{result['iterations']}

Improvements Applied:
{result['improvements_applied']}

Generated Files:
"""

        for file in files:
            path = file.get("path", "unknown")
            message += f"\n- {path}"

        message += f"""

Rationale:
{rationale}

Review:
{review}
"""

        if len(message) > 1900:
            message = message[:1900]

        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"❌ Workflow failed safely: {str(e)}")


bot.run(DISCORD_BOT_TOKEN)
