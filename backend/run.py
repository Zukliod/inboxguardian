from flask import Flask
from app.routes import main  # Import the blueprint

app = Flask(__name__)
app.register_blueprint(main)  # Register the blueprint

if __name__ == '__main__':
    app.run(debug=True)