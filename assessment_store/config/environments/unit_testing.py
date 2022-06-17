"""Flask Unit Testing Environment Configuration."""
from os import path

from config.environments.default import Config
from fsd_tech import configclass


@configclass
class UnitTestingConfig(Config):
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
        Config.FLASK_ROOT, SQLITE_DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
