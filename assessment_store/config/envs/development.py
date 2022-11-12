"""Flask Local Development Environment Configuration."""
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
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEV_SQLALCHEMY_DATABASE_URI = (
        DefaultConfig.SQLALCHEMY_DATABASE_URI + "_DEV"
    )

    SQLALCHEMY_DATABASE_URI = DEV_SQLALCHEMY_DATABASE_URI
