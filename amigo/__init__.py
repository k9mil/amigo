from flask import Flask, g
from flask_socketio import SocketIO
from amigo.config import Config

socketio = SocketIO(cors_allowed_origins = "*")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from amigo.main.routes import main
    from amigo.errors.routes import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    socketio.init_app(app)
    
    return app