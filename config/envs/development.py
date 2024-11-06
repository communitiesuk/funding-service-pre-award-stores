"""Flask configuration."""

import logging
from os import environ

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class DevelopmentConfig(DefaultConfig):
    FSD_LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "development"

    # TODO: MARC - THIS NEEDS TO BE CLEANED UP
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@127.0.0.1:5432/fsd_fund_store_1",  # pragma: allowlist secret
    )
