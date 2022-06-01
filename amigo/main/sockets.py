from flask import request, url_for, g
from flask_socketio import send, emit, join_room, leave_room

from .. import socketio

total_clients = []
usr_data = []
n = 1
rooms = {}

@socketio.on("connect")
def connect():
    total_clients.append(request.sid) 

    if len(total_clients) % 2 == 0:
        emit("redirect", {"url": url_for("main.chat")}, broadcast=True)

@socketio.on("disconnect")
def disconnect():
    total_clients.remove(request.sid)
    print("disconnect")

@socketio.on("join")
def on_join():
    global n
    roomName = "room" + str(n)

    if roomName in rooms:
        pass
    else: 
        rooms[roomName] = []

    if len(rooms[roomName]) <= 1:
        rooms[roomName].append(request.sid)
    else:
        n += 1
        roomName = "room" + str(n)

        if roomName in rooms:
            pass
        else: 
            rooms[roomName] = []

        rooms[roomName].append(request.sid)

    room = roomName
    join_room(room)

@socketio.on("leave")
def on_leave():
    global n
    roomName = "room" + str(n)

    total_clients.remove(request.sid)
    rooms[roomName].remove(request.sid)

    room = roomName
    leave_room(room)

@socketio.on("message")
def handleMessage(msg):
    global roomName
    room = [k for k, v in rooms.items() if request.sid in v]
    sender_id = request.sid
    tmp = []
    tmp.append(msg)
    tmp.append(sender_id)
    send({"msg": tmp}, to=room[0])
