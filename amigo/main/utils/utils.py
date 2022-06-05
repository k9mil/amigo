import re, json, urllib, random

from amigo import redis_conn

from flask import request, session
from urllib.parse import urlencode


def encode_url():
    """
    """
    openid_url = "https://steamcommunity.com/openid/login"

    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.mode": "checkid_setup",
        "openid.return_to": "http://127.0.0.1:5000/process",
        "openid.realm": "http://127.0.0.1:5000"
    }

    encoded_url = (openid_url + "?" + urlencode(params))
    return encoded_url

def get_data():
    """
    """

    steam_id_re = re.compile("https://steamcommunity.com/openid/id/(.*?)$")
    current_user = steam_id_re.search(dict(request.args)["openid.identity"])
    steam_data = get_user_info(current_user.group(1))
    game = obtain_game(steam_data)
    rand_id = random.randint(0,25565)

    redis_conn.hmset(
        rand_id, {"username": steam_data["personaname"].encode('utf-8'), "game": game.encode('utf-8')}
    )

    session["steam_id"] = rand_id
    session["game"] = game

def obtain_game(steam_data):
    """
    """
    if (steam_data["gameextrainfo"]):
        return steam_data["gameextrainfo"]
    elif (steam_data["gameid"]):
        return steam_data["gameid"]

def get_user_info(steam_id):
    """
    """
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=40B868AA0378A7783543346141620CB4&steamids={steam_id}"
    rv = json.load(urllib.request.urlopen(url))

    return rv["response"]["players"][0]