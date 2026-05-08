import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

import discord
from discord.ext import commands

from config import DISCORD_BOT_TOKEN
from orchestrator.workflow import run_workflow

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def _format_list(items: Iterable[Any]) -> str:
    values = [str(item).strip() for item in items if str(item).strip()]
    if not values:
        return "- None"
    return "\n".join(f"- {item}" for item in values)


def _format_bugs(bugs: Iterable[Dict[str, Any]]) -> str:
    formatted: List[str] = []
    for bug in bugs:
        if not isinstance(bug, dict):
            text = str(bug).strip()
            if text:
                formatted.append(f"- **medium**: {text}")
            continue

        severity = str(bug.get("severity", "medium")).strip().lower() or "medium"
        issue = str(bug.get("issue", "")).strip()
        fix = str(bug.get("fix", "")).strip()
        if not issue:
            continue

        line = f"- **{severity}**: {issue}"
        if fix:
            line += f"\n  Fix: {fix}"
        formatted.append(line)

    if not formatted:
        return "- None"
    return "\n".join(formatted)


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
        await ctx.send("## Final Code\nNo code generated.")
        return

    for index, chunk in enumerate(_chunk_text(code), start=1):
        title = "## Final Code" if index == 1 else "## Final Code (continued)"
        message = f"{title}\n```python\n{chunk}\n```"
        if len(message) > DISCORD_MESSAGE_LIMIT:
            message = f"{title}\n```text\n{chunk[:SAFE_MESSAGE_LIMIT]}\n```"
        await ctx.send(message)


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
        state = result.get("state", {})
        iterations = result.get("iterations", 1)
        improvements_applied = bool(state.get("improvements_applied", False))

        message = f"""
✅ Workflow Complete

        summary_message = (
            f"✅ Done in {iterations} iteration(s).\n"
            f"**Improvements applied:** {'Yes' if improvements_applied else 'No'}"
        )
        await ctx.send(summary_message)
        await _send_code(ctx, code_output)

Improvements Applied:
{result['improvements_applied']}

        review_message = (
            "## Reviewer Findings\n"
            f"**Bugs**\n{_format_bugs(review.get('bugs', []))}\n\n"
            f"**Improvements**\n{_format_list(review.get('improvements', []))}\n\n"
            f"**Suggested Fixes**\n{_format_list(review.get('suggested_fixes', []))}"
        )

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
