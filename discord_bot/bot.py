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

from reviewer.project_loader import ProjectLoader
from reviewer.review_cycle import ReviewCycle
from reviewer.file_writer import FileWriter

print("PROJECT REVIEW ENGINE ACTIVE")

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
        "!review_project"
    ):
        return

    try:

        project_path = message.content.replace(
            "!review_project",
            ""
        ).strip()

        if not project_path:

            await message.channel.send(
                "❌ Bitte Projektpfad angeben."
            )

            return

        # -----------------------------------
        # LOAD PROJECT
        # -----------------------------------

        loader = ProjectLoader()

        files = loader.load_project_files(
            project_path
        )

        if not files:

            await message.channel.send(
                "❌ Keine Python-Dateien gefunden."
            )

            return

        review_cycle = ReviewCycle()

        file_writer = FileWriter()

        response = (
            "🧠 **Project Review Results**\n\n"
        )

        total_findings = 0
        total_fixed = 0
        total_written = 0

        # -----------------------------------
        # REVIEW FILES
        # -----------------------------------

        for file_data in files:

            file_path = file_data[
                "file_path"
            ]

            content = file_data[
                "content"
            ]

            # -----------------------------------
            # SKIP READ ERRORS
            # -----------------------------------

            if content.startswith(
                "# FILE_READ_ERROR"
            ):

                response += (
                    f"❌ Fehler beim Lesen:\n"
                    f"{file_path}\n\n"
                )

                continue

            # -----------------------------------
            # REVIEW
            # -----------------------------------

            result = review_cycle.review_file(
                content,
                file_path
            )

            final_findings = result[
                "final_findings"
            ]

            iterations = result[
                "iterations"
            ]

            final_code = result[
                "final_code"
            ]

            fixed_count = 0

            for iteration in iterations:

                fixed_count += len(
                    iteration[
                        "resolved_findings"
                    ]
                )

            initial_findings = 0

            if iterations:

                initial_findings = len(
                    iterations[0][
                        "findings"
                    ]
                )

            total_findings += (
                initial_findings
            )

            total_fixed += fixed_count

            # -----------------------------------
            # WRITE FIXED FILE
            # -----------------------------------

            write_success = False

            if (
                final_code
                and final_code != content
            ):

                file_writer.create_backup(
                    file_path
                )

                write_result = (
                    file_writer.write_file(
                        file_path,
                        final_code
                    )
                )

                write_success = write_result[
                    "success"
                ]

                if write_success:

                    total_written += 1

            # -----------------------------------
            # FILE RESULT
            # -----------------------------------

            response += (
                "============================\n"
            )

            response += (
                f"📄 FILE:\n{file_path}\n\n"
            )

            response += (
                f"⚠️ Findings: "
                f"{initial_findings}\n"
            )

            response += (
                f"✅ Fixed: "
                f"{fixed_count}\n"
            )

            response += (
                f"🚨 Remaining: "
                f"{len(final_findings)}\n"
            )

            response += (
                f"🎯 Success: "
                f"{result['success']}\n"
            )

            response += (
                f"💾 File Updated: "
                f"{write_success}\n\n"
            )

            # -----------------------------------
            # REMAINING FINDINGS
            # -----------------------------------

            if final_findings:

                response += (
                    "🚨 Remaining Findings:\n"
                )

                for finding in final_findings:

                    response += (
                        f"- {finding['title']}\n"
                    )

                response += "\n"

        # -----------------------------------
        # SUMMARY
        # -----------------------------------

        response += (
            "============================\n"
        )

        response += (
            "📊 PROJECT SUMMARY\n\n"
        )

        response += (
            f"📁 Files Reviewed: "
            f"{len(files)}\n"
        )

        response += (
            f"⚠️ Total Findings: "
            f"{total_findings}\n"
        )

        response += (
            f"✅ Total Fixed: "
            f"{total_fixed}\n"
        )

        response += (
            f"💾 Files Updated: "
            f"{total_written}\n"
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

    except Exception as e:

        await message.channel.send(
            f"❌ Fehler:\n```python\n{str(e)}\n```"
        )


client.run(TOKEN)
