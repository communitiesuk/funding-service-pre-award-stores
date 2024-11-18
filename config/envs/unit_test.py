"""Flask Local Development Environment Configuration."""

import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class UnitTestConfig(Config):
    #  Application Config
    SECRET_KEY = "test"  # pragma: allowlist secret

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG
