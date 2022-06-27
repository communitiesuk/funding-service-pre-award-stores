"""Flask Dev Pipeline Environment Configuration."""
from os import environ
from os import path

from config.environments.default import DefaultConfig
from fsd_utils import configclass


@configclass
class DevConfig(DefaultConfig):

    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + path.join(DefaultConfig.FLASK_ROOT, "sqlite.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
