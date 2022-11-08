"""Flask Unit Testing Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class UnitTestingConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ENV = "unit_test"

    # APIs
    APPLICATION_STORE_API_HOST = CommonConfig.TEST_APPLICATION_STORE_API_HOST
    ACCOUNT_STORE_API_HOST = CommonConfig.TEST_ACCOUNT_STORE_API_HOST
    NOTIFICATION_SERVICE_HOST = CommonConfig.TEST_NOTIFICATION_SERVICE_HOST

    # Security
    FORCE_HTTPS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WARN_IF_QUERIES_OVER_MS = 5
