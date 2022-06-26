import os

class Config:
    """
        todo
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    AUTH_KEY = os.environ.get('AUTH_KEY')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    STEAM_KEY = os.environ.get('STEAM_KEY')
