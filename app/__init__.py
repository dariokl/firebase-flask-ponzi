from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    # Get the type of configuration from config.py
    config_module = config[config_name]

    app.config.from_object(config_module)
    config_module.init_app(app)

    # Initialize blueprints
    from .ponzi import ponzibp as ponzi_blueprint
    app.register_blueprint(ponzi_blueprint)

    return app