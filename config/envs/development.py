"""Flask Local Development Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class DevelopmentConfig(Config):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    FLASK_ENV = "development"

    # Logging
    FSD_LOG_LEVEL = logging.INFO
    # ---------------
    # AWS Config
    # ---------------
    AWS_SECRET_ACCESS_KEY = AWS_SQS_SECRET_ACCESS_KEY = "test_secret_key"  # pragma: allowlist secret
    AWS_ACCESS_KEY_ID = AWS_SQS_ACCESS_KEY_ID = "test_access_key"  # pragma: allowlist secret
    AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = "fsd-queue-test"
    AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL = "test_secondary_url"
    AWS_SQS_REGION = AWS_REGION = "eu-west-2"

    # ---------------
    # S3 Config
    # ---------------
    AWS_MSG_BUCKET_NAME = "fsd-notification-bucket"
