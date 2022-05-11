from flask import Flask, render_template, Blueprint, redirect, request, url_for
from flask_socketio import send, emit, join_room, leave_room
from unnamed.config import Config
from urllib.parse import urlencode
from furl import furl
from .. import socketio

import re, urllib, json

main = Blueprint("main", __name__)

total_clients = []
n = 1
rooms = {}

@socketio.on("message")
def handleMessage(msg):
    global roomName
    room = [k for k, v in rooms.items() if request.sid in v]
    send(msg, to=room[0])

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

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/waiting")
def waiting():
    return render_template("waiting.html")

@main.route("/auth_game")
def auth_game():
    steam_id_re = re.compile("https://steamcommunity.com/openid/id/(.*?)$")
    match = steam_id_re.search(dict(request.args)["openid.identity"])
    steam_data = get_user_info(match.group(1))

    try:
        if (steam_data["gameextrainfo"]):
            print(steam_data["gameextrainfo"])
        elif (steam_data["gameid"]):
            print(steam_data["gameid"])
    except KeyError:
        return redirect(url_for("errors.notfound"))
        
    return redirect(url_for("main.waiting"))

@main.route("/chat")
def chat():
    return render_template("chat.html")

@main.route("/authenticate")
def authenticate():
    openid_url = "https://steamcommunity.com/openid/login"

    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.mode": "checkid_setup",
        "openid.return_to": "http://127.0.0.1:5000/auth_game",
        "openid.realm": "http://127.0.0.1:5000"
    }

    auth_url = openid_url + "?" + urlencode(params)

    return redirect(auth_url)

def get_user_info(steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=40B868AA0378A7783543346141620CB4&steamids={steam_id}"
    rv = json.load(urllib.request.urlopen(url))

    return rv["response"]["players"][0]
