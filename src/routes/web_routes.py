"""HTML page routes."""
from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")
