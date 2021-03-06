from flask import Flask, request, url_for, session, request
from flask_socketio import send, emit, join_room, leave_room

from amigo import redis_conn
from amigo.main.utils.events_utils import check_conditions, hget
from amigo.main.utils.other_utils import remove_data

from .. import socketio

@socketio.on("process")
def process() -> None:
    """This function handles the main connection, and essentially only runs in the waiting room,
    as when it runs on the /chat/ page, there's two exceptions and a pass is thrown.
    Architecture will be improved.

    Adds the request.sid to the redis hash, then it iterates through all hashes and finds a user 
    playing the same game that is not the current user.

    Args:
        None

    Returns:
        None
    """

    redis_conn.hset(session["steam_id"], "sid", request.sid)
    users = check_conditions()

    if users:
        emit("process", {"url": url_for("main.chat")}, to=users)

@socketio.on("disconnect")
def disconnect() -> None:
    """Removes the user from the redis pool, as well as removes their current session
    in the global namespace (waiting room).

    Args:
        None

    Returns:
        None
    """

    status = hget(session["steam_id"], "available")

    if status == "True":
        remove_data()

@socketio.on("disconnect", namespace="/chat")
def disconnect_chat() -> None:
    """Removes the user from the redis pool, as well as removes their
    current session in the chat namespace.

    Args:
        None

    Returns:
        None
    """

    status = hget(session["steam_id"], "available")
    socketio.emit("exit", to=session.get("room"))

    if status == "False":
        remove_data()

@socketio.on("join")
def join() -> None:
    """Creates a session variable 'room', and then joins the room.

    Args:
        None

    Returns:
        None
    """

    session["room"] = hget(session["steam_id"], "room")
    room: str = session.get("room")
    join_room(room)

@socketio.on("leave")
def leave() -> None:
    """Retrieves the room from the session, and then leaves the room.
    (be careful)

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

    msg_data: list[str, int] = [msg, request.sid]
    send({"msg": msg_data}, to=session.get("room"))
