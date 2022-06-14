"""Flask Dev Pipeline Environment Configuration."""
from os import environ
from os import path

from config.environments.default import Config


class DevConfig(Config):

    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + path.join(Config.FLASK_ROOT, "sqlite.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
