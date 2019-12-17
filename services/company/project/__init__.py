from flask import Flask

def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': None})

    return app
