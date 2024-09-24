"""Flask Dev Pipeline Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class DevConfig(Config):
    #  Application Config
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.INFO
