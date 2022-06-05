import re, json, urllib, random

from amigo import redis_conn

from flask import request, session
from urllib.parse import urlencode


def encode_url() -> str:
    """Returns an encoded URL with all the necessary parameters for OpenID authentication.

    Args:
        None

    Returns:
        encoded_url: The URL with all params.
    """

    openid_url: str = "https://steamcommunity.com/openid/login"

    params: dict[str, str] = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.mode": "checkid_setup",
        "openid.return_to": "http://127.0.0.1:5000/process",
        "openid.realm": "http://127.0.0.1:5000"
    }

    encoded_url: str = (openid_url + "?" + urlencode(params))
    return encoded_url

def get_data() -> None:
    """Primary function for obtaining steam data & current game. Creates a redis hash with the username & game data.

    Appends to session.

    Args:
        None
    
    Returns:
        None
    """

    steam_id_re = re.compile("https://steamcommunity.com/openid/id/(.*?)$")
    current_user = steam_id_re.search(dict(request.args)["openid.identity"])
    steam_data = get_user_info(current_user.group(1))
    game: str = obtain_game(steam_data)
    rand_id: int = random.randint(0,25565)

    redis_conn.hmset(
        rand_id, {"username": steam_data["personaname"].encode('utf-8'), "game": game.encode('utf-8')}
    )

    session["steam_id"] = rand_id
    session["game"] = game

def obtain_game(steam_data) -> str:
    """Obtains game data, some games only have 'gameid' which is a unique identifier, and some games have
    'gameextrainfo' which is the full game name.

    Args:
        steam_data: 

    Returns:
        steam_data["variable"]: A string containing either the name, or the id of the game.
    """

    if (steam_data["gameextrainfo"]):
        return steam_data["gameextrainfo"]
    elif (steam_data["gameid"]):
        return steam_data["gameid"]

def get_user_info(steam_id) -> dict[str, str]:
    """
    """
    
    url: str = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=40B868AA0378A7783543346141620CB4&steamids={steam_id}"
    rv: dict[str, list] = json.load(urllib.request.urlopen(url))

    return rv["response"]["players"][0]