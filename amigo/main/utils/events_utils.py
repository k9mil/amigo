from ast import Str
from flask import request, session

from amigo import redis_conn


users: list[int] = []


def check_conditions() -> list[int]:
    """Iterates over every hash and looks for an appropriate pair for each person in the waiting 
    room, if found, creates a room and returns the lits of users.

    Args:
        None

    Returns:
        users: List of SocketIO unique user identifiers.
    """

    user_steam_id: int = session["steam_id"]
    user_game: str = session["game"]

    for r_hash in redis_conn.scan_iter("*"):
        current_game: str = hget(r_hash, "game")
        current_sid: int = hget(r_hash, "sid")
        current_availability: str = hget(r_hash, "available")

        cond_list = (
            current_game == user_game
            and str(user_steam_id) != r_hash.decode('utf-8')
            and current_availability == "True"
        )

        if cond_list:
            users.clear()
            users.extend([current_sid, request.sid])
            create_room(current_sid, r_hash, request.sid)

            redis_conn.hset(user_steam_id, "available", "False")
            redis_conn.hset(r_hash.decode('utf-8'), "available", "False")

            return users

def create_room(current_sid: int, r_hash: bytes, request_sid: int) -> None:
    """Creates a room for both users that will be transferred, and stores it in redis.

    Args:
        current_sid: The request SocketIO identifier (of the partner found).
        r_hash: The current object in iteration.
        request_sid: The request SocketIO identifier (of the current user).

    Returns:
        None
    """

    redis_conn.hset(session["steam_id"], "room", request_sid + current_sid)
    redis_conn.hset(r_hash.decode('utf-8'), "room", request_sid + current_sid)

def hget(key1, key2):
    """Takes in two keys for hget(), and returns a decoded value from redis.

    Args:
        key1: The current 'r_hash' in iteration.
        key2: The variable to search for.

    Returns:
        value.decode('utf-8'): The value in utf-8 format.
    """

    value = redis_conn.hget(key1, key2)
    return value.decode('utf-8')
