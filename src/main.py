"""Entry point for the Flask app."""
from src import create_app
from src.config import DevConfig

app = create_app(DevConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
