"""Flask configuration."""
from os import environ
from pathlib import Path

from config.mappings import assessment_mapping
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

    COF_R2W2_ASSESSMENT_MAPPING = (
        assessment_mapping.cof_r2w2_assessment_mapping
    )
