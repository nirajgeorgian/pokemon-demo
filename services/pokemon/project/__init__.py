# services/pokemon/project/__init__.py

import os

from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()

def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.pokemon import pokemon_blueprint
    app.register_blueprint(pokemon_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
