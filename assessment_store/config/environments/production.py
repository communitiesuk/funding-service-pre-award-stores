"""Flask Production Environment Configuration."""
from config.environments.default import DefaultConfig
from fsd_tech import configclass


@configclass
class ProductionConfig(DefaultConfig):
    pass
