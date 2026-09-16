"""Flask application factory."""
from flask import Flask
from .config import Config


def create_app(config_class=Config):
    """Create and configure the Flask app."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_class)

    from .routes.web_routes import web_bp
    from .routes.api_routes import api_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
