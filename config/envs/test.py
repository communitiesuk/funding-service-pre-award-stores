"""Flask Test Environment Configuration."""

from fsd_utils import configclass

from config.envs.aws import AwsConfig


@configclass
class TestConfig(AwsConfig):
    pass
