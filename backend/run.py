import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to InboxGuardian!"

if __name__ == "__main__":
    # Use Railway's dynamic port assignment
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT is not set
    app.run(host="0.0.0.0", port=port)