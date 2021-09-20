# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from datetime import datetime
import os

from flask import Flask



# Instantiate Flask extensions
# mail = Mail()

# Initialize Flask Application
def create_app(extra_config_settings={}):
    """Create a Flask application.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings
    app.config.from_object('app.settings')
    # Load environment specific settings
    app.config.from_object('app.local_settings')
    # Load extra settings from extra_config_settings param
    app.config.update(extra_config_settings)


    # Register blueprints
    from .views import register_blueprints
    register_blueprints(app)


    return app

