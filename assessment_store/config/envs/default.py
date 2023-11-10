"""Flask configuration."""
import json
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

    # ---------------
    # Database
    # ---------------

    SQLALCHEMY_DATABASE_URI = environ["DATABASE_URL"].replace(
        "postgres://", "postgresql://"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"future": True}

    ASSESSMENT_MAPPING_CONFIG = fund_round_to_assessment_mapping

    # ---------------
    # AWS Config
    # ---------------
    if "PRIMARY_QUEUE_URL" in environ:
        AWS_REGION = environ.get("AWS_REGION")
        AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = environ.get("PRIMARY_QUEUE_URL")
        AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL = environ.get(
            "DEAD_LETTER_QUEUE_URL"
        )
    elif "VCAP_SERVICES" in environ:
        vcap_services = json.loads(environ["VCAP_SERVICES"])
        if "aws-sqs-queue" in vcap_services:
            sqs_credentials = vcap_services["aws-sqs-queue"][0]["credentials"]
            AWS_REGION = sqs_credentials["aws_region"]
            AWS_ACCESS_KEY_ID = sqs_credentials["aws_access_key_id"]
            AWS_SECRET_ACCESS_KEY = sqs_credentials["aws_secret_access_key"]
            AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = sqs_credentials[
                "primary_queue_url"
            ]
            AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL = sqs_credentials[
                "secondary_queue_url"
            ]
    else:
        AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
        AWS_REGION = environ.get("AWS_REGION")
        AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = environ.get(
            "AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL"
        )
        AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL = environ.get(
            "AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL"
        )
    AWS_DLQ_MAX_RECIEVE_COUNT = int(
        environ.get("AWS_DLQ_MAX_RECIEVE_COUNT", 3)
    )

    # ---------------
    # SQS Config
    # ---------------
    SQS_WAIT_TIME = int(
        environ.get("SQS_WAIT_TIME", 2)
    )  # max time to wait (in sec) before returning
    SQS_BATCH_SIZE = int(
        environ.get("SQS_BATCH_SIZE", 1)
    )  # MaxNumber Of Messages to process
    SQS_VISIBILITY_TIME = int(
        environ.get("SQS_VISIBILITY_TIME", 1)
    )  # time for message to temporarily invisible to others (in sec)
    SQS_RECEIVE_MESSAGE_CYCLE_TIME = int(
        environ.get("SQS_RECEIVE_MESSAGE_CYCLE_TIME", 60)
    )  # Run the job every 'x' seconds
