"""A tethics bot for Tethics.

Uses an airtable list of interested people to create matches at random.

Add this bot to your server as an administrator w/ this link:
https://discord.com/oauth2/authorize?client_id=787061094769885216&scope=bot&permissions=8
"""
import random
import os
from typing import List, Literal, TypedDict

import discord

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)


class DiscordUserNotFound(Exception):
    pass


def get_active_users(text_channel) -> List[discord.Member]:
    """Get active users in a given discord text channel."""

    active_users = []
    for m in text_channel.members:
        if m.status.name in ["online", "dnd"] and m.bot == False:
            active_users.append(m)

    return active_users


@client.event
async def on_ready():
    """on_ready is called when the discord bot first loads."""
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(msg: discord.Message):
    if msg.content.strip() == "!1:1":
        # get discord user from message
        author = msg.author
        print(msg)
        print(msg.channel)
        print(msg.author)
        online_users = get_active_users(msg.channel)

        match = random.choice(online_users)

        message = "{} and {} have matched for a 1:1!".format(
            author.mention, match.mention
        )
        await msg.channel.send(message)

    elif msg.content.startswith("!1:1"):
        await msg.channel.send(
            "Sorry, I didn't get that. I don't have a help command either, so "
            + "go pester Andrew to build one."
        )
        return


client.run(TOKEN)
