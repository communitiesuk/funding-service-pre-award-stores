"""Flask Local Development Environment Configuration."""

import logging

from fsd_utils import CommonConfig, configclass

from config.envs.default import DefaultConfig


@configclass
class DevelopmentConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ENV = "development"

    FSD_LOG_LEVEL = logging.INFO

    # APIs
    APPLICATION_STORE_API_HOST = CommonConfig.TEST_APPLICATION_STORE_API_HOST

    # Security
    FORCE_HTTPS = False

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
