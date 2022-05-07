from flask import Flask
from unnamed.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from unnamed.main.routes import main
    from unnamed.errors.routes import errors

    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app