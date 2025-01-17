"""Flask Dev Pipeline Environment Configuration."""

import logging
from os import getenv

from fsd_utils import configclass

from pre_award.config.envs.aws import AwsConfig


@configclass
class DevConfig(AwsConfig):
    # Logging
    FSD_LOG_LEVEL = logging.INFO

    SESSION_COOKIE_DOMAIN = getenv("SESSION_COOKIE_DOMAIN")

    # assess dev config
    REDIS_INSTANCE_NAME = "funding-service-magic-links-dev"
