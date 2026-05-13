import discord
import os

from reviewer.reviewer_engine import ReviewerEngine

TOKEN = os.getenv("DISCORD_TOKEN")

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

    code_example = """
import hashlib
import random

users = {}

def create_user(name, password, roles=[]):
    hashed = hashlib.md5(password.encode()).hexdigest()

    user_id = random.randint(1, 5)

    users[user_id] = {
        "name": name,
        "password": hashed,
        "roles": roles
    }

    return user_id

def calculate_average(numbers):
    total = 0

    for i in range(len(numbers)):
        total += numbers[i]

    return total / len(numbers)

create_user("admin", "123456")
print(calculate_average([]))
"""

    engine = ReviewerEngine()

    engine.add_finding(
        title="Unsafe MD5 Usage",
        description="MD5 is insecure for password hashing",
        severity="high",
        file_path="auth.py",
        line=8,
        code_snippet="hashlib.md5(password.encode())",
        category="security"
    )

    engine.add_finding(
        title="Mutable Default Argument",
        description="Using mutable default arguments can cause shared state bugs",
        severity="medium",
        file_path="auth.py",
        line=6,
        code_snippet="roles=[]",
        category="bug"
    )

    engine.add_finding(
        title="Possible Division By Zero",
        description="len(numbers) can be zero",
        severity="medium",
        file_path="math_utils.py",
        line=24,
        code_snippet="return total / len(numbers)",
        category="bug"
    )

    engine.add_finding(
        title="Weak Random ID Generation",
        description="Small random range can create collisions",
        severity="medium",
        file_path="auth.py",
        line=10,
        code_snippet="random.randint(1, 5)",
        category="security"
    )

    findings = engine.get_findings()

    response = (
        "🧠 **Reviewer Results**\n\n"
        f"⚠️ Findings Found: {len(findings)}\n\n"
    )

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
            "-----------------------------------\n\n"
        )

    response += (
        "```python\n"
        f"{code_example}\n"
        "```"
    )

    if len(response) > 1900:
        response = response[:1900] + "\n\n...[truncated]"

    await message.channel.send(response)


client.run(TOKEN)
