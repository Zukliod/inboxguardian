from flask import Flask
from app.analytics import analytics  # Import analytics blueprint
from app.routes import main  # Import existing routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  # Register routes
    app.register_blueprint(analytics, url_prefix='/analytics')  # Register analytics blueprint
    
    @app.route('/favicon.ico')
    def favicon():
        favicon_path = os.path.join(app.static_folder, "favicon.ico")
        if os.path.exists(favicon_path):
            return send_from_directory(app.static_folder, "favicon.ico")
        else:
            return "Favicon not found", 404
    
    @app.route("/", methods=["HEAD"])
    def head_root():
        return "", 200
    
    return app