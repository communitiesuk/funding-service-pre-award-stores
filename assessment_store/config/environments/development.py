"""Flask Local Development Environment Configuration."""
from os import environ
from os import path

from config.environments.default import DefaultConfig
from fsd_tech import configclass


@configclass
class DevelopmentConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "development"

    # APIs
    APPLICATION_STORE_API_HOST = "application_store"
    ACCOUNT_STORE_API_HOST = "account_store"
    FUND_STORE_API_HOST = "fund_store"
    ROUND_STORE_API_HOST = "round_store"
    NOTIFICATION_SERVICE_HOST = "notification_service"

    # Security
    FORCE_HTTPS = False

    # Database
    SQLITE_DB_NAME = "sqlite.db"
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + path.join(DefaultConfig.FLASK_ROOT, SQLITE_DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
