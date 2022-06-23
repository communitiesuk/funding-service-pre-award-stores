"""Flask Test Environment Configuration."""
from os import environ

from config.environments.default import DefaultConfig
from fsd_utils import configclass


@configclass
class TestConfig(DefaultConfig):

    SECRET_KEY = environ.get("SECRET_KEY", "test")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL").replace(
        "postgres://", "postgresql://"
    )
