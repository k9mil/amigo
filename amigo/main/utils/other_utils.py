from flask import session
from amigo import redis_conn


def remove_data():
    """
    """
    
    redis_conn.delete(session["steam_id"])
    session.pop("steam_id", None)
    session.pop("game", None)
    session.clear()