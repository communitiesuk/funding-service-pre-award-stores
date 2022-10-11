"""Flask Dev Pipeline Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class DevConfig(DefaultConfig):

    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
