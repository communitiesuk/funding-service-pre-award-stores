"""Flask configuration."""

import logging
from distutils.util import strtobool
from os import environ
from pathlib import Path

from fsd_utils import CommonConfig, configclass

from assessment_store.config.mappings.assessment_mapping_fund_round import (
    fund_round_to_assessment_mapping,
)


@configclass
class DefaultConfig(object):
    #  Application Config
    FLASK_ENV = CommonConfig.FLASK_ENV
    SECRET_KEY = CommonConfig.SECRET_KEY
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)

    # Logging
    FSD_LOG_LEVEL = logging.WARNING

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/pre_award_stores",  # pragma: allowlist secret
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"future": True}

    ASSESSMENT_MAPPING_CONFIG = fund_round_to_assessment_mapping

    #  APIs
    TEST_FUND_STORE_API_HOST = "fund_store"
    TEST_ACCOUNT_STORE_API_HOST = "account_store"
    USE_LOCAL_DATA = strtobool(environ.get("USE_LOCAL_DATA", "False"))
    FUND_STORE_API_HOST = environ.get("FUND_STORE_API_HOST", TEST_FUND_STORE_API_HOST)
    ACCOUNT_STORE_API_HOST = environ.get("ACCOUNT_STORE_API_HOST", TEST_ACCOUNT_STORE_API_HOST)

    # Notification Service
    NOTIFY_TEMPLATE_SUBMIT_APPLICATION = "APPLICATION_RECORD_OF_SUBMISSION"
    NOTIFY_TEMPLATE_INCOMPLETE_APPLICATION = "INCOMPLETE_APPLICATION_RECORDS"
    NOTIFY_TEMPLATE_APPLICATION_DEADLINE_REMINDER = "APPLICATION_DEADLINE_REMINDER"
    NOTIFY_TEMPLATE_APPLICATION_DEADLINE_REMINDER = environ.get(
        "NOTIFY_TEMPLATE_APPLICATION_DEADLINE_REMINDER",
        NOTIFY_TEMPLATE_APPLICATION_DEADLINE_REMINDER,
    )
    NOTIFY_TEMPLATE_EOI_PASS = "Full pass"
    NOTIFY_TEMPLATE_EOI_PASS_W_CAVEATS = "Pass with caveats"

    # Account Store Endpoints
    ACCOUNT_ENDPOINT = CommonConfig.ACCOUNT_ENDPOINT
    ACCOUNTS_ENDPOINT = "/accounts"

    # Fund Store Endpoints
    FUNDS_ENDPOINT = CommonConfig.FUNDS_ENDPOINT
    FUND_ENDPOINT = CommonConfig.FUND_ENDPOINT
    FUND_ROUNDS_ENDPOINT = CommonConfig.ROUNDS_ENDPOINT
    FUND_ROUND_ENDPOINT = CommonConfig.ROUND_ENDPOINT
    FUND_ROUND_APPLICATION_SECTIONS_ENDPOINT = (
        "/funds/{fund_id}/rounds/{round_id}/sections/application?language={language}"
    )
    FUND_ROUND_APPLICATION_REMINDER_STATUS = "/funds/{round_id}/application_reminder_status?status=true"
    FUND_ROUND_EOI_SCHEMA_ENDPOINT = FUND_STORE_API_HOST + "/funds/{fund_id}/rounds/{round_id}/eoi_decision_schema"

    DOCUMENT_UPLOAD_SIZE_LIMIT = 2 * 1024 * 1024

    # Application Store
    APPLICATION_STORE_API_HOST = CommonConfig.APPLICATION_STORE_API_HOST
    APPLICATIONS_ENDPOINT = CommonConfig.APPLICATIONS_ENDPOINT
    APPLICATION_ENDPOINT = CommonConfig.APPLICATION_ENDPOINT

    # Assessment frontend details
    ASSESSMENT_FRONTEND_HOST = environ.get("ASSESSMENT_FRONTEND_HOST")
    ASSESSMENT_APPLICATION_ENDPOINT = "/assess/application/{application_id}"

    # ---------------
    # AWS Overall Config
    # ---------------
    AWS_ACCESS_KEY_ID = AWS_SQS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = AWS_SQS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = AWS_SQS_REGION = environ.get("AWS_REGION")
    AWS_ENDPOINT_OVERRIDE = environ.get("AWS_ENDPOINT_OVERRIDE")

    # ---------------
    # S3 Config
    # ---------------
    AWS_MSG_BUCKET_NAME = environ.get("AWS_MSG_BUCKET_NAME")
    AWS_BUCKET_NAME = environ.get("AWS_BUCKET_NAME")
