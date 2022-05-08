from flask import Flask
from flask_socketio import SocketIO
from unnamed.config import Config

socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from unnamed.main.routes import main
    from unnamed.errors.routes import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    socketio.init_app(app)
    
    return app