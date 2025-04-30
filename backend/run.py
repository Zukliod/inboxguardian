import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.app.routes import main

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://harshit:tWv50MSjul8cyyN0RmspiJYeqDguoDIC@dpg-d06i4mruibrs73ekeiq0-a.singapore-postgres.render.com/inboxguardian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Register routes
app.register_blueprint(main)

# Handle favicon requests
@app.route('/favicon.ico')
def favicon():
    favicon_path = os.path.join(app.static_folder, "favicon.ico")
    if os.path.exists(favicon_path):
        return send_from_directory(app.static_folder, "favicon.ico")
    else:
        return "Favicon not found", 404

@app.route("/")
def serve_frontend():
    if os.path.exists(os.path.join(app.static_folder, "index.html")):
        return send_from_directory(app.static_folder, "index.html")
    else:
        return "Frontend is not built yet. Please build the frontend and place it in the 'frontend/build' directory.", 200

# Handle HEAD requests for "/"
@app.route("/", methods=["HEAD"])
def head_root():
    return "", 200

@app.errorhandler(404)
def not_found(e):
    if os.path.exists(os.path.join(app.static_folder, "index.html")):
        return send_from_directory(app.static_folder, "index.html")
    else:
        return "Page not found, and the frontend is not built yet.", 404

# Example model (replace with your actual models)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)