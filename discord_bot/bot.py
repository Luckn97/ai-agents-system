import sys
from pathlib import Path
from typing import Any, Iterable, List

import discord
from discord.ext import commands

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow_async
from utils.logger import get_logger

logger = get_logger(__name__)

DISCORD_MESSAGE_LIMIT = 2000
SAFE_MESSAGE_LIMIT = 1900

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def _format_list(items: Iterable[Any]) -> str:
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


async def _send_chunks(ctx: commands.Context, text: str) -> None:
    for chunk in _chunk_text(text):
        await ctx.send(chunk)


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
        result = await run_workflow_async(task_text)

        code_result = result.get("code", {})
        review = result.get("review", {})
        state = result.get("state", {})
        iterations = result.get("iterations", 1)
        improvements_applied = bool(state.get("improvements_applied", False))

        code_output = str(code_result.get("code", "No code generated."))
        rationale = str(code_result.get("rationale", ""))

        await ctx.send(
            f"✅ Done.\n"
            f"**Iterations:** {iterations}\n"
            f"**Improvements applied:** {'Yes' if improvements_applied else 'No'}"
        )
        await _send_code(ctx, code_output)

        await _send_chunks(ctx, f"## Rationale\n{rationale or 'No rationale provided.'}")

        review_message = (
            "## Review\n"
            f"**Bugs**\n{_format_list(review.get('bugs', []))}\n\n"
            f"**Improvements**\n{_format_list(review.get('improvements', []))}\n\n"
            f"**Suggested Fixes**\n{_format_list(review.get('suggested_fixes', []))}"
        )
        await _send_chunks(ctx, review_message)

    except Exception as exc:
        logger.exception("Workflow failed")
        await ctx.send(f"❌ Workflow failed safely: {exc}")


if not DISCORD_BOT_TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is not set.")

bot.run(DISCORD_BOT_TOKEN)
