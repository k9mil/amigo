from flask import request, url_for
from flask_socketio import send, emit, join_room, leave_room

from amigo import redis_conn

from .. import socketio

@socketio.on("connect")
def connect():
    if len(total_clients) % 2 == 0:
        emit("redirect", {"url": url_for("main.chat")}, broadcast=True)

@socketio.on("disconnect")
def disconnect():
    print("disconnect")

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
