"""Flask Production Environment Configuration."""
from config.environments.default import Config
from fsd_tech import configclass


@configclass
class ProductionConfig(Config):
    pass
