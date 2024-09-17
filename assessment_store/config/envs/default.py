"""Flask configuration."""
from os import environ
from pathlib import Path

from config.mappings.assessment_mapping_fund_round import (
    fund_round_to_assessment_mapping,
)
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class DefaultConfig:
    # ---------------
    #  General App Config
    # ---------------

    SECRET_KEY = CommonConfig.SECRET_KEY
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    FLASK_ENV = CommonConfig.FLASK_ENV
    FORCE_HTTPS = CommonConfig.FORCE_HTTPS
    FSD_LOG_LEVEL = CommonConfig.FSD_LOG_LEVEL

    # ---------------
    # APIs Config: contains api hosts (set in manifest.yml)
    # ---------------

    # Application Store
    APPLICATION_STORE_API_HOST = CommonConfig.APPLICATION_STORE_API_HOST
    APPLICATIONS_ENDPOINT = CommonConfig.APPLICATIONS_ENDPOINT
    APPLICATION_ENDPOINT = CommonConfig.APPLICATION_ENDPOINT

    # Account Store
    ACCOUNT_STORE_API_HOST = CommonConfig.ACCOUNT_STORE_API_HOST
    ACCOUNTS_ENDPOINT = CommonConfig.ACCOUNTS_ENDPOINT
    ACCOUNT_ENDPOINT = CommonConfig.ACCOUNT_ENDPOINT

    # Fund Store
    FUND_STORE_API_HOST = CommonConfig.FUND_STORE_API_HOST
    FUNDS_ENDPOINT = CommonConfig.FUNDS_ENDPOINT
    FUND_ENDPOINT = CommonConfig.FUND_ENDPOINT + "?use_short_name={use_short_name}"

    ASSESSMENT_FRONTEND_HOST = environ.get("ASSESSMENT_FRONTEND_HOST")
    ASSESSMENT_APPLICATION_ENDPOINT = "/assess/application/{application_id}"

    # ---------------
    # Database
    # ---------------

    SQLALCHEMY_DATABASE_URI = environ["DATABASE_URL"].replace("postgres://", "postgresql://")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"future": True}

    ASSESSMENT_MAPPING_CONFIG = fund_round_to_assessment_mapping

    # ---------------
    # AWS Config
    # ---------------
    AWS_REGION = environ.get("AWS_REGION")
    AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = environ.get("PRIMARY_QUEUE_URL")
    AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL = environ.get("DEAD_LETTER_QUEUE_URL")
    AWS_SQS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SQS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_SQS_REGION = AWS_REGION = environ.get("AWS_REGION")
    AWS_ENDPOINT_OVERRIDE = environ.get("AWS_ENDPOINT_OVERRIDE")

    # ---------------
    # S3 Config
    # ---------------
    AWS_MSG_BUCKET_NAME = environ.get("AWS_MSG_BUCKET_NAME")
    # ---------------
    # Task Executor Config
    # ---------------
    TASK_EXECUTOR_MAX_THREAD = int(environ.get("TASK_EXECUTOR_MAX_THREAD", 5))  # max amount of threads

    # ---------------
    # SQS Config
    # ---------------
    SQS_WAIT_TIME = int(environ.get("SQS_WAIT_TIME", 2))  # max time to wait (in sec) before returning
    SQS_BATCH_SIZE = int(environ.get("SQS_BATCH_SIZE", 1))  # MaxNumber Of Messages to process
    SQS_VISIBILITY_TIME = int(
        environ.get("SQS_VISIBILITY_TIME", 1)
    )  # time for message to temporarily invisible to others (in sec)
    SQS_RECEIVE_MESSAGE_CYCLE_TIME = int(
        environ.get("SQS_RECEIVE_MESSAGE_CYCLE_TIME", 60)
    )  # Run the job every 'x' seconds

    # ---------------
    # SQS Config
    # ---------------
    AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL = environ.get("AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL")
    AWS_SQS_NOTIF_APP_SECONDARY_QUEUE_URL = environ.get("AWS_SQS_NOTIF_APP_SECONDARY_QUEUE_URL")
