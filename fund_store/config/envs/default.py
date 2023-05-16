"""Flask configuration."""
import logging
from os import environ
from os import getenv
from pathlib import Path

from distutils.util import strtobool
from fsd_utils import configclass


@configclass
class DefaultConfig(object):
    #  Application Config
    SECRET_KEY = environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = environ.get("SESSION_COOKIE_NAME")
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    FLASK_ENV = environ.get("FLASK_ENV")

    # Logging
    FSD_LOG_LEVEL = logging.WARNING

    # Frontend
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    FORCE_OPEN = strtobool(getenv("FORCE_OPEN", "False"))

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    )
