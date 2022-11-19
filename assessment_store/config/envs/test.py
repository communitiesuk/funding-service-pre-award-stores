"""Flask Test Environment Configuration."""
from os import environ

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class TestConfig(DefaultConfig):

    SECRET_KEY = environ.get("SECRET_KEY", "test")

