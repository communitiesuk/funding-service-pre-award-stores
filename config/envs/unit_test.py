"""Flask Local Development Environment Configuration."""

import logging
from os import environ

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "test"  # pragma: allowlist secret

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/pre_award_stores_test",  # pragma: allowlist secret
    )
