"""Flask Test Environment Configuration."""
from os import environ

from config.environments.default import Config


class TestConfig(Config):

    SECRET_KEY = environ.get("SECRET_KEY", "test")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL").replace(
        "postgres://", "postgresql://"
    )
