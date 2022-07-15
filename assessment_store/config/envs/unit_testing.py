"""Flask Unit Testing Environment Configuration."""
from os import path

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class UnitTestingConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "testing"

    # APIs
    APPLICATION_STORE_API_HOST = "application_store"
    ACCOUNT_STORE_API_HOST = "account_store"
    FUND_STORE_API_HOST = "fund_store"
    ROUND_STORE_API_HOST = "round_store"
    NOTIFICATION_SERVICE_HOST = "notification_service"

    # Security
    FORCE_HTTPS = False

    # Database
    SQLITE_DB_NAME = "test_sqlite.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(
        DefaultConfig.FLASK_ROOT, SQLITE_DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
