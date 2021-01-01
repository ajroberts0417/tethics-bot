"""A tethics bot for Tethics.

Uses an airtable list of interested people to create matches at random.

Add this bot to your server as an administrator w/ this link:
https://discord.com/oauth2/authorize?client_id=787061094769885216&scope=bot&permissions=8
"""
import random
import re
import os
from typing import List, Literal, TypedDict

import discord

from ratings_service import (
    get_thing,
    like_thing,
    dislike_thing,
    get_things,
    get_user_ratings,
)

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True
client = discord.Client(intents=intents)

UP_ARROW = r"\N{up arrow}"
DOWN_ARROW = r"\N{down arrow}"


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
        online_users = get_active_users(msg.channel)

        match = random.choice(online_users)

        message = "{} and {} have matched for a 1:1!".format(
            author.mention, match.mention
        )
        await msg.channel.send(message)

    elif msg.content.startswith("!rate"):
        # send a message with a thing to rate, and instructions
        thing = get_thing()

        message = (
            ":chart_with_upwards_trend: **Rate this thing:** :chart_with_downwards_trend:\n\n"
            "**<| {} |>**\n\n"
            "*Reply with :arrow_up: to like // Reply with :arrow_down: to dislike*"
        ).format(thing)

        message = await msg.channel.send(message)
        await message.add_reaction("⬆")
        await message.add_reaction("⬇")

    elif msg.content.startswith("!things"):
        things = get_things()
        message = ":bar_chart:  **List of things** :pencil:\n\n"
        for thing in things:
            ratio = round(
                float(thing["likes"]) / float(thing["dislikes"] + thing["likes"]) * 100,
                1,
            )
            desc = "**{name}** - {ratio}% - Likes: {likes} // Dislikes: {dislikes}\n".format(
                ratio=ratio, **thing
            )
            message += desc
        await msg.channel.send(message)

    elif msg.content.startswith("!ratings"):
        username = str(msg.author)
        ratings = get_user_ratings(username)
        message = "**{}'s Ratings**\n\n".format(msg.author.mention)
        for rating in ratings:
            name = rating["thing"]["name"]
            emoji = "✅" if rating["like"] else "❌"

            desc = f"**{name}** - {emoji}"
            message += desc
        await msg.channel.send(message)

    elif msg.content.startswith("!1:1"):
        await msg.channel.send(
            "Sorry, I didn't get that. I don't have a help command either, so "
            + "go pester Andrew to build one."
        )


# @client.event
# async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
#     # process any Ratings related messages
#     msg = reaction.message
#     if reaction.me or user.bot:
#         # skip cases where a bot is reacting
#         return
#     breakpoint()
#     if msg.author.bot and "Rate this thing" in msg.content:
#         thing_search = re.search("\*\*<\| (.*) \|>\*\*", msg.content)
#         thing = thing_search.group(1)
#         if reaction.emoji.name == "arrow_up":
#             ok = like_thing(thing, str(user))
#         if reaction.emoji.name == "arrow_down":
#             ok = dislike_thing(thing, str(user))


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    # get msg
    user = payload.member
    if user.bot:
        # skip cases where a bot is reacting
        return
    msg = discord.utils.get(client.cached_messages, id=payload.message_id)
    if msg.author.bot and "Rate this thing" in msg.content:
        thing_search = re.search("\*\*<\| (.*) \|>\*\*", msg.content)
        thing = thing_search.group(1)
        if payload.emoji.name == "⬆":
            ok = like_thing(thing, str(user))
        if payload.emoji.name == "⬇":
            ok = dislike_thing(thing, str(user))


client.run(TOKEN)
