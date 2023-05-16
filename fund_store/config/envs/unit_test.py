"""Flask Local Development Environment Configuration."""
import logging
from os import environ

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "test"
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@127.0.0.1:5432/fsd_fund_store_unit_test",
    )
