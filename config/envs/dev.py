"""Flask Dev Pipeline Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.aws import AwsConfig


@configclass
class DevConfig(AwsConfig):
    # Logging
    FSD_LOG_LEVEL = logging.INFO
