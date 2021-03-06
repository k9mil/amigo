from flask import Flask
from flask_socketio import SocketIO
from amigo.config import Config

import redis

redis_conn = redis.Redis(host = "localhost", port = 6379, db = 0)
socketio = SocketIO(cors_allowed_origins = "*")

def create_app(config_class=Config) -> Flask:
    """Creates an application factory and sets everything up. Returns a flask object.

    Args:
        config_class: The configuration file.

    Returns:
        app: The flask object.

    """
    
    app: Flask = Flask(__name__)
    app.config.from_object(Config)

    from amigo.main.routes import main
    from amigo.errors.routes import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    socketio.init_app(app)
    
    return app