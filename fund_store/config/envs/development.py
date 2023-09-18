"""Flask Local Development Environment Configuration."""
import logging
from os import environ

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class DevelopmentConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "development"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@127.0.0.1:5432/fsd_fund_store_1",  # pragma: allowlist secret
    )
