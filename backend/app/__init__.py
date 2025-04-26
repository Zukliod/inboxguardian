from flask import Flask
from app.analytics import analytics  # Import analytics blueprint
from app.routes import main  # Import existing routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  # Register routes
    app.register_blueprint(analytics, url_prefix='/analytics')  # Register analytics blueprint
    return app