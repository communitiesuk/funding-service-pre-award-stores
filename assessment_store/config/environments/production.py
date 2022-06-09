"""Flask Production Environment Configuration."""
from config.environments.default import Config


class ProductionConfig(Config):
    pass

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
