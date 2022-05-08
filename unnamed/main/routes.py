from flask import Flask, render_template, Blueprint, redirect, request
from flask_socketio import send
from unnamed.config import Config
from urllib.parse import urlencode
from .. import socketio

import re, urllib, json

main = Blueprint("main", __name__)

@socketio.on("message")
def handleMessage(msg):
    print("Message: " + msg)
    send(msg, broadcast = True)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/waiting")
def waiting():
    return render_template("waiting.html")

@main.route("/chat")
def chat():
    try:
        steam_id_re = re.compile("https://steamcommunity.com/openid/id/(.*?)$")
        match = steam_id_re.search(dict(request.args)["openid.identity"])
        q = match.group(1)
        print(q)
        steam_data = get_user_info(q)
        print(steam_data)
        what = steam_data["steamid"]
        print(what)
    except KeyError:
        return render_template("chat.html")

    return render_template("chat.html")

@main.route("/authenticate")
def authenticate():
    openid_url = "https://steamcommunity.com/openid/login"

    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.mode": "checkid_setup",
        "openid.return_to": "http://127.0.0.1:5000/chat",
        "openid.realm": "http://127.0.0.1:5000"
    }

    auth_url = openid_url + "?" + urlencode(params)
    print(auth_url)

    return redirect(auth_url)

def get_user_info(steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=40B868AA0378A7783543346141620CB4&steamids={steam_id}"
    print(url)
    rv = json.load(urllib.request.urlopen(url))

    return rv["response"]["players"][0]
