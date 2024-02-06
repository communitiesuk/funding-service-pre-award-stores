"""Flask Unit Testing Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class UnitTestingConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ENV = "unit_test"

    # APIs
    APPLICATION_STORE_API_HOST = CommonConfig.TEST_APPLICATION_STORE_API_HOST
    ACCOUNT_STORE_API_HOST = CommonConfig.TEST_ACCOUNT_STORE_API_HOST

    # Security
    FORCE_HTTPS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WARN_IF_QUERIES_OVER_MS = 5

    SQLALCHEMY_DATABASE_URI = DefaultConfig.SQLALCHEMY_DATABASE_URI + "_UNIT_TEST"

    AWS_ACCESS_KEY_ID = "test_access_id"
    AWS_SECRET_ACCESS_KEY = "test_secret_key"  # pragma: allowlist secret
    AWS_REGION = "eu-west-2"
    AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = "test_primary_url"
    AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL = "test_secondary_url"
