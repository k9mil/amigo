from flask import request, url_for, session
from flask_socketio import send, emit, join_room, leave_room

from amigo import redis_conn

from .. import socketio

users = []

@socketio.on("connect")
def connect():
    """
    """

    try:
        redis_conn.hset(session["steam_id"], "sid", request.sid)

        for k in redis_conn.scan_iter("*"):
            current_game = redis_conn.hget(k, "game").decode('utf-8')
            current_steam_id = session["steam_id"]
            current_sid = redis_conn.hget(k, "sid").decode('utf-8')

            if current_game == session.get("game") and str(current_steam_id) != str(k.decode('utf-8')):
                users.append(current_sid)
                users.append(request.sid)
                emit("redirect", {"url": url_for("main.chat")}, to=users)
    except Exception:
        pass

@socketio.on("disconnect")
def disconnect():
    """
    """

    redis_conn.delete(session["steam_id"])
    session.pop("steam_id", None)
    redis_conn.flushall()

@socketio.on("join")
def join():
    """
    """

    session["room"] = "room"
    room = session.get("room")
    join_room(room)

@socketio.on("leave")
def leave():
    """
    """
    
    room = session.get("room")
    leave_room(room)

@socketio.on("message")
def message(msg):
    """
    """

    sender_id = request.sid
    room = session.get("room")
    tmp = []
    tmp.append(msg)
    tmp.append(sender_id)
    send({"msg": tmp}, to=room)
