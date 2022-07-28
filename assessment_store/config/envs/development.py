"""Flask Local Development Environment Configuration."""
from os import environ
from os import path

from config.envs.default import DefaultConfig
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class DevelopmentConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ENV = "development"

    # APIs
    APPLICATION_STORE_API_HOST = CommonConfig.TEST_APPLICATION_STORE_API_HOST
    ACCOUNT_STORE_API_HOST = CommonConfig.TEST_ACCOUNT_STORE_API_HOST
    FUND_STORE_API_HOST = CommonConfig.TEST_FUND_STORE_API_HOST
    NOTIFICATION_SERVICE_HOST = CommonConfig.TEST_NOTIFICATION_SERVICE_HOST

    # Security
    FORCE_HTTPS = False

    # Database
    SQLITE_DB_NAME = "sqlite.db"
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + path.join(DefaultConfig.FLASK_ROOT, SQLITE_DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
