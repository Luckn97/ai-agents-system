import sys
from pathlib import Path
from typing import Iterable, List

import discord
from discord.ext import commands

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow
from utils.logger import get_logger

logger = get_logger(__name__)

DISCORD_MESSAGE_LIMIT = 2000
SAFE_MESSAGE_LIMIT = 1900

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def _format_list(items: Iterable[str]) -> str:
    values = [str(item).strip() for item in items if str(item).strip()]
    if not values:
        return "- None"
    return "\n".join(f"- {item}" for item in values)


def _chunk_text(text: str, limit: int = SAFE_MESSAGE_LIMIT) -> List[str]:
    if len(text) <= limit:
        return [text]

    chunks: List[str] = []
    remaining = text

    while remaining:
        if len(remaining) <= limit:
            chunks.append(remaining)
            break

        split_at = remaining.rfind("\n", 0, limit)
        if split_at <= 0:
            split_at = limit

        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip("\n")

    return chunks


async def _send_code(ctx: commands.Context, code: str) -> None:
    if not code.strip():
        await ctx.send("## Generated Code\nNo code generated.")
        return

    for index, chunk in enumerate(_chunk_text(code), start=1):
        title = "## Generated Code" if index == 1 else "## Generated Code (continued)"
        message = f"{title}\n```python\n{chunk}\n```"
        if len(message) > DISCORD_MESSAGE_LIMIT:
            message = f"{title}\n```text\n{chunk[:SAFE_MESSAGE_LIMIT]}\n```"
        await ctx.send(message)


@bot.event
async def on_ready() -> None:
    logger.info("Logged in as %s", bot.user)


@bot.command(name="task")
async def run_task(ctx: commands.Context, *, task_text: str) -> None:
    await ctx.send("⚙️ Task received. Running multi-agent workflow...")

    try:
        result = run_workflow(task_text)

        code_result = result.get("code", {})
        review = result.get("review", {})
        iterations = result.get("iterations", 1)

        code_output = str(code_result.get("code", "No code generated."))
        rationale = str(code_result.get("rationale", ""))

        await ctx.send(f"✅ Done in {iterations} iteration(s).")
        await _send_code(ctx, code_output)

        if rationale:
            for chunk in _chunk_text(f"## Rationale\n{rationale}"):
                await ctx.send(chunk)

        review_message = (
            "## Review\n"
            f"**Bugs**\n{_format_list(review.get('bugs', []))}\n\n"
            f"**Improvements**\n{_format_list(review.get('improvements', []))}\n\n"
            f"**Suggested Fixes**\n{_format_list(review.get('suggested_fixes', []))}"
        )

        for chunk in _chunk_text(review_message):
            await ctx.send(chunk)

    except Exception as exc:
        logger.exception("Workflow failed")
        await ctx.send(f"❌ Workflow failed safely: {exc}")


if not DISCORD_BOT_TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is not set.")

bot.run(DISCORD_BOT_TOKEN)
