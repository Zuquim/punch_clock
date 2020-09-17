class Config(object):
    # Flask config
    FLASK_APP = "punch_clock.py"
    DEBUG = False
    TESTING = False
    SECRET_KEY = "Super-S3CR3T-key"
    SERVER_NAME = "zuquim.local"
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    WTF_CSRF_CHECK_DEFAULT = False
    SESSION_COOKIE_SECURE = True

    # Logging config
    LOG_PATH = "./log"
    LOG_LEVEL = 10
    LOGFILE_LEVEL = 10

    # DB config
    SQLITE_DB_PATH = "/var/db"
    SQLITE_DB_FILE = "punch_clock.sqlite"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}/{SQLITE_DB_FILE}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_NAME = "PunchClock"
    DB_USERNAME = "clock"
    DB_PASSWORD = "Punch#T1m3"


class ProductionConfig(Config):
    ENV = "production"

    # Preventing malfunction when working without SSL
    SESSION_COOKIE_SECURE = False

    # Logging config
    LOG_PATH = "/var/log"
    LOG_LEVEL = 30
    LOGFILE_LEVEL = 20


class DevelopmentConfig(Config):
    ENV = "development"

    # Flask config
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SERVER_NAME = "zuquim.local:5000"

    # DB Config
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    DB_NAME = "PunchClock_dev"


class TestingConfig(Config):
    ENV = "testing"

    # Flask config
    TESTING = True
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False

    # DB config
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    DB_NAME = "PunchClock_dev"
