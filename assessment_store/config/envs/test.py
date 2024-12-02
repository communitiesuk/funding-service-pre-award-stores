"""Flask Test Environment Configuration."""

from os import environ

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class TestConfig(DefaultConfig):
    SECRET_KEY = environ.get("SECRET_KEY", "test")
