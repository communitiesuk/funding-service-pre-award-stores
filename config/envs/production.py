"""Flask Production Environment Configuration."""

from fsd_utils import configclass

from config.envs.aws import AwsConfig


@configclass
class ProductionConfig(AwsConfig):
    pass
