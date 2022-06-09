"""Flask Dev Pipeline Environment Configuration."""
from os import environ
from os import path

from config.environments.default import Config


class DevConfig(Config):

    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    """
    Database
    """

    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + path.join(Config.FLASK_ROOT, "sqlite.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """
    Gov PaaS
    """

    # If VCAP_SERVICES are required use the following to parse
    # service params (Redis example given)
    #
    # from config.utils import VcapServices
    # from os import environ
    # VCAP_SERVICES = VcapServices.from_env_json(environ.get("VCAP_SERVICES"))
    # REDIS_INSTANCE_NAME = "funding-service-example-dev"
    # REDIS_INSTANCE_URI = VCAP_SERVICES.get_service_credentials_value(
    #     "redis", REDIS_INSTANCE_NAME, "uri"
    # )
