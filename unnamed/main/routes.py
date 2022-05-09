from flask import Flask, render_template, Blueprint, redirect, request, url_for
from flask_socketio import send, emit
from unnamed.config import Config
from urllib.parse import urlencode
from furl import furl
from .. import socketio

import re, urllib, json

main = Blueprint("main", __name__)

clients = []

@socketio.on("message")
def handleMessage(msg):
    send(msg, broadcast = True)

@socketio.on("connect")
def connect():
    clients.append(request.sid)
    print(clients)
    emit('my response', {'data': 'Connected'})

@socketio.on("disconnect")
def disconnect():
    clients.remove(request.sid)

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
