"""Flask Local Development Environment Configuration."""

import logging
from os import environ

from fsd_utils import CommonConfig, configclass

from config.envs.default import DefaultConfig as Config


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "test"  # pragma: allowlist secret

    # APIs
    APPLICATION_STORE_API_HOST = CommonConfig.TEST_APPLICATION_STORE_API_HOST
    ACCOUNT_STORE_API_HOST = CommonConfig.TEST_ACCOUNT_STORE_API_HOST
    FUND_STORE_API_HOST = Config.TEST_FUND_STORE_API_HOST

    # Security
    FORCE_HTTPS = False

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    # Database
    WARN_IF_QUERIES_OVER_MS = 5
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/pre_award_stores_test",  # pragma: allowlist secret
    )

    # ---------------
    # AWS Config
    # ---------------
    AWS_SECRET_ACCESS_KEY = AWS_SQS_SECRET_ACCESS_KEY = "test_secret_key"  # pragma: allowlist secret
    AWS_ACCESS_KEY_ID = AWS_SQS_ACCESS_KEY_ID = "test_access_key"  # pragma: allowlist secret
    USE_LOCAL_DATA = True
    AWS_SQS_REGION = AWS_REGION = "eu-west-2"

    # ---------------
    # S3 Config
    # ---------------
    AWS_MSG_BUCKET_NAME = "fsd-notification-bucket"
