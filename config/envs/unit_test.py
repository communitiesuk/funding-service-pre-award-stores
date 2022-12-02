"""Flask Local Development Environment Configuration."""
import logging

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI + "_UNIT_TEST"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
