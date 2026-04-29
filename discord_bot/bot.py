import sys
import json
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


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="task")
async def run_task(ctx: commands.Context, *, task_text: str):
    await ctx.send("⚙️ Task received. Running multi-agent workflow...")

    try:
        result = run_workflow(task_text)

        raw_code = result.get("code", "")
        review = result.get("review", {})
        iterations = result.get("iterations", 1)

        try:
            parsed_code = json.loads(raw_code)

            code_output = parsed_code.get("code", raw_code)
            rationale = parsed_code.get("rationale", "")

        except Exception:
            code_output = raw_code
            rationale = ""

        bugs = review.get("bugs", [])
        improvements = review.get("improvements", [])
        fixes = review.get("suggested_fixes", [])

        message = (
            f"✅ Done in {iterations} iteration(s).\n\n"
            f"## GENERATED CODE\n"
            f"```python\n{code_output}\n```\n"
        )

        if rationale:
            message += f"**Rationale:** {rationale}\n\n"

        message += (
            f"## REVIEW\n"
            f"**Bugs:** {bugs}\n"
            f"**Improvements:** {improvements}\n"
            f"**Suggested Fixes:** {fixes}"
        )

        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"❌ Workflow failed safely: {str(e)}")


bot.run(DISCORD_BOT_TOKEN)
