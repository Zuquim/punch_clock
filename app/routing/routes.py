"""Logged-in page routes."""
from time import strftime

from flask import current_app as app
from flask import (
    Blueprint,
    jsonify,
)

from app import __version__, setup_logging
from app.models import User, PunchClock
from app.routing import row2dict

log = setup_logging("main", app.config)

# Blueprint Configuration
main_bp = Blueprint(
    "main_bp",
    __name__,
    template_folder=app.config.get("TEMPLATE_DIR"),
    static_folder=app.config.get("STATIC_DIR"),
)


@main_bp.route("/", methods=["GET"])
def index():
    """Route made for testing purposes."""
    return (
        jsonify(
            {
                "datetime": strftime("%Y-%m-%d %H:%M:%S"),
                "message": f"Punch Clock v{__version__}",
                "path": "/",
                "version": __version__,
            }
        ),
        200,
    )
