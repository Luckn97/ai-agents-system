import discord
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from reviewer.python_ast_analyzer import PythonASTAnalyzer
from reviewer.autofix_engine import AutoFixEngine

print("NEW AST + DIFF AUTOFIX REVIEWER ACTIVE")

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError(
        "DISCORD_TOKEN environment variable missing"
    )

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if not message.content.startswith("!task"):
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
    # AST REVIEW
    # -----------------------------------

    try:

        analyzer = PythonASTAnalyzer(
            code=code_example,
            file_path="user_code.py"
        )

        findings = analyzer.analyze()

    except Exception as e:

        await message.channel.send(
            f"❌ Fehler bei der Analyse:\n```python\n{str(e)}\n```"
        )

        return

    # -----------------------------------
    # AUTOFIX
    # -----------------------------------

    try:

        autofix_engine = AutoFixEngine()

        autofix_result = autofix_engine.apply_fixes(
            code_example
        )

        fixed_code = autofix_result[
            "fixed_code"
        ]

        fixes_applied = autofix_result[
            "fixes_applied"
        ]

        diff_output = autofix_result[
            "diff"
        ]

    except Exception as e:

        await message.channel.send(
            f"❌ Fehler beim AutoFix:\n```python\n{str(e)}\n```"
        )

        return

    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    response = (
        "🧠 **Reviewer Results**\n\n"
        f"⚠️ Findings Found: {len(findings)}\n\n"
    )

    # -----------------------------------
    # FINDINGS
    # -----------------------------------

    if not findings:

        response += "✅ Keine Probleme gefunden.\n"

    else:

        for finding in findings:

            response += (
                "-----------------------------------\n"
                f"🆔 ID: {finding['id']}\n"
                f"📌 Title: {finding['title']}\n"
                f"🔥 Severity: {finding['severity']}\n"
                f"🎯 Confidence: {finding['confidence']}\n"
                f"📄 File: {finding['file_path']}\n"
                f"📍 Line: {finding['line']}\n"
                f"📂 Category: {finding['category']}\n"
                f"📝 Description: {finding['description']}\n"
                f"💻 Snippet: {finding['code_snippet']}\n"
                "-----------------------------------\n\n"
            )

    # -----------------------------------
    # AUTOFIX RESULTS
    # -----------------------------------

    response += "\n🛠️ **AutoFix Results**\n\n"

    if fixes_applied:

        for fix in fixes_applied:

            response += f"✅ {fix}\n"

    else:

        response += (
            "Keine automatischen Fixes angewendet.\n"
        )

    # -----------------------------------
    # DIFF OUTPUT
    # -----------------------------------

    response += (
        "\n📦 **Generated Diff:**\n"
        "```diff\n"
        f"{diff_output[:1200]}\n"
        "```"
    )

    # -----------------------------------
    # DISCORD LIMIT PROTECTION
    # -----------------------------------

    if len(response) > 1900:

        response = (
            response[:1900]
            + "\n\n...[truncated]"
        )

    await message.channel.send(response)


client.run(TOKEN)
