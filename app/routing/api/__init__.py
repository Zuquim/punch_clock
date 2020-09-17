from flask import current_app as app
from flask import Blueprint

from app import setup_logging

# Blueprint Configuration
api_bp = Blueprint(
    "api_bp",
    __name__,
    template_folder=app.config.get("TEMPLATE_DIR"),
    static_folder=app.config.get("STATIC_DIR"),
)

# Logging setup
api_log = setup_logging("api", app.config)
