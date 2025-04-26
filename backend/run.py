import os
from flask import Flask, send_from_directory
from app.routes import main  # Import the API blueprint

# Create the Flask app
app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")

# Register the API blueprint
app.register_blueprint(main)

# Serve frontend files
@app.route("/")
def serve_frontend():
    """
    Serve the frontend index.html file.
    This assumes the frontend build files are located in the `frontend/build` directory.
    """
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def not_found(e):
    """
    Handle 404 errors by serving the frontend index.html file.
    This ensures React or Flutter web routing works correctly.
    """
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    # Get the port from environment variables (default to 5000)
    port = int(os.environ.get("PORT", 5000))

    # Run the app in debug mode if specified in environment variables
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    # Start the Flask app
    app.run(host="0.0.0.0", port=port, debug=debug)