"""Flask Test Environment configuration."""

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class TestConfig(DefaultConfig):
    pass
