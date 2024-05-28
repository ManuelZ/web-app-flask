# External imports
from flask import Flask
from flask_cors import CORS

# Local imports
from backend.api import bp as api_bp
from backend.config import Config
from backend.extensions import db
from backend.extensions import migrate


def create_app(config_class=Config):
    """ """

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
