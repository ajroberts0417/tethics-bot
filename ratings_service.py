import requests
import os

RATINGS_ENDPOINT = "https://fierce-beyond-97330.herokuapp.com/graphql"
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")


def get_thing():
    """Get a random thing from the Ratings backend."""
    gql = "query { getThing { name }}"
    payload = {"query": gql}

    response = requests.post(RATINGS_ENDPOINT, data=payload)

    data = response.json()
    return data["data"]["getThing"]["name"]


def get_things():
    """Get all the things from the Ratings backend."""
    gql = "query { things {name likes dislikes}}"
    payload = {"query": gql}

    response = requests.post(RATINGS_ENDPOINT, data=payload)

    data = response.json()
    return data["data"]["things"]


def get_user_ratings(username):
    """Get all the things from the Ratings backend."""
    gql = """query {{ ratings(username: "{}") {{thing {{name}} like}}}}""".format(
        username
    )
    payload = {"query": gql}

    response = requests.post(RATINGS_ENDPOINT, data=payload)
    data = response.json()
    return data["data"]["ratings"]


def like_thing(thing, discord_user_id):
    """Increment a user's rating for the thing."""

    gql = """
        mutation IncrementRating{{
            incrementRating(thingName: "{}", discordUserId: "{}", botToken: "{}")
            {{ ok }}
        }}
    """.format(
        thing, discord_user_id, BOT_API_TOKEN
    )
    payload = {"query": gql}

    response = requests.post(RATINGS_ENDPOINT, data=payload)

    data = response.json()
    return data["data"]["incrementRating"]["ok"]


def dislike_thing(thing, discord_user_id):
    """Decrement a user's rating for the thing."""
    gql = """
        mutation DecrementRating{{
            decrementRating(thingName: "{}", discordUserId: "{}", botToken: "{}")
            {{ ok }}
        }}
    """.format(
        thing, discord_user_id, BOT_API_TOKEN
    )
    payload = {"query": gql}

    response = requests.post(RATINGS_ENDPOINT, data=payload)

    data = response.json()
    return data["data"]["decrementRating"]["ok"]
