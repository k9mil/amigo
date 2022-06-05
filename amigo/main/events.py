from flask import request, url_for, session
from flask_socketio import send, emit, join_room, leave_room

from amigo import redis_conn

from .. import socketio

users: list[None] = []

@socketio.on("connect")
def connect() -> None:
    """This function handles the main connection, and essentially only runs in the waiting room,
    as when it runs on the /chat/ page, there's two exceptions and a pass is thrown. Architecture will be improved.

    Adds the request.sid to the redis hash, then it iterates through all hashes and finds a user playing the same game
    that is not the current user.

    Args:
        None

    Returns:
        None
    """

    try:
        redis_conn.hset(session["steam_id"], "sid", request.sid)

        for k in redis_conn.scan_iter("*"):
            current_game: str = redis_conn.hget(k, "game").decode('utf-8')
            current_steam_id: int = session["steam_id"]
            current_sid: int = redis_conn.hget(k, "sid").decode('utf-8')

            if current_game == session.get("game") and str(current_steam_id) != str(k.decode('utf-8')):
                users.append(current_sid)
                users.append(request.sid)
                
                emit("redirect", {"url": url_for("main.chat")}, to=users)
    except Exception:
        pass

@socketio.on("disconnect")
def disconnect() -> None:
    """Removes the user from the redis pool, as well as removes their current session.

    Args:
        None

    Returns:
        None
    """

    redis_conn.delete(session["steam_id"])
    session.pop("steam_id", None)
    redis_conn.flushall()

@socketio.on("join")
def join() -> None:
    """Creates a session variable 'room', and then joins the said room.

    Args:
        None

    Returns:
        None
    """

    session["room"] = "room"
    room: str = session.get("room")
    join_room(room)

@socketio.on("leave")
def leave() -> None:
    """Retrieves the room from the session, and then leaves the room.

    Args:
        None

    Returns:
        None
    """
    
    room: str = session.get("room")
    leave_room(room)

@socketio.on("message")
def message(msg: str) -> None:
    """Handles messages server-side, gets the room from the session and creates
    a list containing the request.sid, a unique SocketID identifier, and the message.
    This is to differentiate between sender, and the receiver.

    Args:
        msg: User input from the text box.

    Returns:
        None
    """

    sender_id: int = request.sid
    room: str = session.get("room")
    tmp: list[None] = []

    tmp.append(msg)
    tmp.append(sender_id)

    send({"msg": tmp}, to=room)
