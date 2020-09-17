from os import access, environ, mkdir, W_OK
from os.path import exists

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logzero import setup_logger

__version__ = "0.1.0"


def setup_logging(name: str, config: dict):
    if not exists(config["LOG_PATH"]):
        mkdir(config["LOG_PATH"])
    else:
        if not access(config["LOG_PATH"], W_OK):
            raise PermissionError(f"Write permission denied to {config['LOG_PATH']}")

    return setup_logger(
        name=name,
        level=config["LOG_LEVEL"],
        logfile=f"{config['LOG_PATH']}/punch_clock.log",
        fileLoglevel=config["LOGFILE_LEVEL"],
        maxBytes=512000,
        backupCount=4,
    )


db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    if environ.get("ENV") == "production":
        app.config.from_object("config.ProductionConfig")
    elif environ.get("ENV") == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    log = setup_logging("app", app.config)
    log.info(f"Starting Punch Clock v{__version__} (env={app.config['ENV']})")
    log.debug(f"Logging in: {app.config['LOG_PATH']}/")

    db.init_app(app)

    with app.app_context():
        # Import routes
        from app.routing import api
        from app.routing import routes
        from app.routing.api import user, punchclock

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(api.api_bp)

        # Create tables for our models
        db.create_all()

        return app
