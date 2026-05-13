import discord
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from reviewer.review_cycle import ReviewCycle

print("ADVANCED REVIEW CYCLE ACTIVE")

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

    iterations = result[
        "iterations"
    ]

    final_findings = result[
        "final_findings"
    ]

    success = result[
        "success"
    ]

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    response = (
        "🧠 **Advanced Review Cycle Results**\n\n"
    )

    response += (
        f"🔄 Iterations: "
        f"{len(iterations)}\n"
    )

    response += (
        f"✅ Success: "
        f"{success}\n"
    )

    response += (
        f"🚨 Final Findings: "
        f"{len(final_findings)}\n\n"
    )

    # -----------------------------------
    # ITERATIONS
    # -----------------------------------

    for iteration_data in iterations:

        response += (
            f"\n============================\n"
        )

        response += (
            f"🔁 ITERATION "
            f"{iteration_data['iteration']}\n"
        )

        response += (
            f"📌 Status: "
            f"{iteration_data['status']}\n"
        )

        response += (
            f"⚠️ Findings: "
            f"{len(iteration_data['findings'])}\n"
        )

        response += (
            f"✅ Resolved: "
            f"{len(iteration_data['resolved_findings'])}\n"
        )

        response += (
            f"🚨 Remaining: "
            f"{len(iteration_data['remaining_findings'])}\n\n"
        )

        # -----------------------------------
        # FIXES
        # -----------------------------------

        if iteration_data[
            "fixes_applied"
        ]:

            response += (
                "🛠️ Applied Fixes\n"
            )

            for fix in iteration_data[
                "fixes_applied"
            ]:

                response += (
                    f"✅ {fix}\n"
                )

        # -----------------------------------
        # DIFF
        # -----------------------------------

        if iteration_data["diff"]:

            response += (
                "\n📦 Diff\n"
                "```diff\n"
                f"{iteration_data['diff'][:600]}\n"
                "```\n"
            )

    # -----------------------------------
    # FINAL FINDINGS
    # -----------------------------------

    if final_findings:

        response += (
            "\n🚨 FINAL REMAINING FINDINGS\n\n"
        )

        for finding in final_findings:

            response += (
                f"❌ {finding['title']} "
                f"(Line {finding['line']})\n"
            )

    else:

        response += (
            "\n🎉 No remaining findings detected.\n"
        )

    # -----------------------------------
    # DISCORD LIMIT
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
