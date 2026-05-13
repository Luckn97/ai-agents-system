import discord
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from reviewer.review_cycle import ReviewCycle

print("RE-REVIEW ENGINE ACTIVE")

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError(
        "DISCORD_TOKEN environment variable missing"
    )

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(
    intents=intents
)


@client.event
async def on_ready():

    print(
        f"Logged in as {client.user}"
    )


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if not message.content.startswith(
        "!task"
    ):
        return

    # -----------------------------------
    # USER INPUT
    # -----------------------------------

    user_prompt = message.content.replace(
        "!task",
        ""
    ).strip()

    # -----------------------------------
    # CODE EXTRACTION
    # -----------------------------------

    if "CODE:" in user_prompt:

        code_example = user_prompt.split(
            "CODE:"
        )[1].strip()

    else:

        await message.channel.send(
            "❌ Kein CODE:-Block gefunden."
        )

        return

    # -----------------------------------
    # REVIEW CYCLE
    # -----------------------------------

    try:

        cycle = ReviewCycle()

        result = cycle.run(
            code_example
        )

    except Exception as e:

        await message.channel.send(
            f"❌ Fehler im Review Cycle:\n```python\n{str(e)}\n```"
        )

        return

    initial_findings = result[
        "initial_findings"
    ]

    remaining_findings = result[
        "remaining_findings"
    ]

    resolved_findings = result[
        "resolved_findings"
    ]

    fixes_applied = result[
        "fixes_applied"
    ]

    diff_output = result[
        "diff"
    ]

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    response = (
        "🧠 **Review Cycle Results**\n\n"
    )

    # -----------------------------------
    # INITIAL FINDINGS
    # -----------------------------------

    response += (
        f"⚠️ Initial Findings: "
        f"{len(initial_findings)}\n"
    )

    response += (
        f"✅ Resolved Findings: "
        f"{len(resolved_findings)}\n"
    )

    response += (
        f"🚨 Remaining Findings: "
        f"{len(remaining_findings)}\n\n"
    )

    # -----------------------------------
    # RESOLVED FINDINGS
    # -----------------------------------

    if resolved_findings:

        response += (
            "✅ **Resolved Findings**\n\n"
        )

        for finding in resolved_findings:

            response += (
                f"✔️ {finding['title']} "
                f"(Line {finding['line']})\n"
            )

    # -----------------------------------
    # REMAINING FINDINGS
    # -----------------------------------

    if remaining_findings:

        response += (
            "\n🚨 **Remaining Findings**\n\n"
        )

        for finding in remaining_findings:

            response += (
                "-----------------------------------\n"
                f"🆔 ID: {finding['id']}\n"
                f"📌 Title: {finding['title']}\n"
                f"🔥 Severity: {finding['severity']}\n"
                f"📍 Line: {finding['line']}\n"
                f"📝 Description: {finding['description']}\n"
                "-----------------------------------\n\n"
            )

    # -----------------------------------
    # AUTOFIX RESULTS
    # -----------------------------------

    response += (
        "\n🛠️ **Applied Fixes**\n\n"
    )

    if fixes_applied:

        for fix in fixes_applied:

            response += f"✅ {fix}\n"

    else:

        response += (
            "Keine automatischen Fixes angewendet.\n"
        )

    # -----------------------------------
    # DIFF
    # -----------------------------------

    response += (
        "\n📦 **Generated Diff**\n"
        "```diff\n"
        f"{diff_output[:1000]}\n"
        "```"
    )

    # -----------------------------------
    # LIMIT PROTECTION
    # -----------------------------------

    if len(response) > 1900:

        response = (
            response[:1900]
            + "\n\n...[truncated]"
        )

    await message.channel.send(
        response
    )


client.run(TOKEN)
