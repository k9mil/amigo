from flask import request, url_for, session
from flask_socketio import send, emit, join_room, leave_room

from amigo import redis_conn

from .. import socketio

@socketio.on("connect")
def connect():
    redis_conn.hset(session["id"], "sid", request.sid)

    for k in redis_conn.scan_iter():
        current_game = redis_conn.hget(k, "game").decode('utf-8')
        current_id = session["id"]
        current_sid = redis_conn.hget(k, "sid").decode('utf-8')

        if current_game == session.get("game") and current_id != session.get("id"):
            print("__debug__real__")
        elif current_game == session.get("game"):
            print("__debug__fake__")
            # emit("redirect", {"url": url_for("main.chat")}, to=current_sid, include_self=True)

@socketio.on("disconnect")
def disconnect():
    redis_conn.delete(session["id"])
    session.pop("id", None)

@socketio.on("join")
def on_join():
    join_room("room")

@socketio.on("leave")
def on_leave():
    leave_room("room")

@socketio.on("message")
def handleMessage(msg):
    global roomName
    room = [k for k, v in rooms.items() if request.sid in v]
    sender_id = request.sid
    tmp = []
    tmp.append(msg)
    tmp.append(sender_id)
    send({"msg": tmp}, to=room[0])
