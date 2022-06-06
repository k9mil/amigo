from flask import request, session

from amigo import redis_conn


users: list[int] = []


def check_conditions() -> list[int]:
    """Iterates over every hash and looks for an appropriate pair for each person in the waiting room,
    if found, creates a room and returns the lits of users.

    Args:
        None

    Returns:
        users: List of SocketIO unique user identifiers.
    """

    for hash in redis_conn.scan_iter("*"):
        current_game: str = redis_conn.hget(hash, "game").decode('utf-8')
        current_sid: int = redis_conn.hget(hash, "sid").decode('utf-8')
        current_steam_id: int = session["steam_id"]

        if current_game == session.get("game") and str(current_steam_id) != hash.decode('utf-8'):
            users.extend([current_sid, request.sid])
            create_room(current_sid, hash, request.sid)

            return users

def create_room(current_sid: int, hash: bytes, request_sid: int) -> None:
    """Creates a room for both users that will be transferred, and stores it in redis.

    Args:
        current_sid: The request SocketIO identifier (of the partner found).
        hash: The current object in iteration.
        request_sid: The request SocketIO identifier (of the current user).

    Returns:
        None
    """

    redis_conn.hset(session["steam_id"], "room", request_sid + current_sid)
    redis_conn.hset(hash.decode('utf-8'), "room", request_sid + current_sid)
